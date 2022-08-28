from collections import defaultdict

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme

from star_burger import settings
from .models import Order
from .models import OrderElements
from .models import Product
from .models import ProductCategory
from .models import Restaurant
from .models import RestaurantMenuItem


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


class OrderElementsInline(admin.TabularInline):
    model = OrderElements
    readonly_fields = ["price_in_order"]
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ]
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide'
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>',
                           url=obj.image.url)

    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html(
            '<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>',
            edit_url=edit_url, src=obj.image.url)

    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderElementsInline]
    list_display = ["firstname", "lastname", "address", "status", "payment",
                    "cooking_restaurant", "status"]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.price_in_order = instance.product.price
            instance.save()

    def response_change(self, request, obj):
        res = super().response_change(request, obj)
        if "next" in request.GET:
            if url_has_allowed_host_and_scheme(
                request.GET['next'],
                allowed_hosts=settings.ALLOWED_HOSTS
            ):
                return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def render_change_form(self, request, context, *args, **kwargs):
        order = kwargs['obj']

        restaurant_menu_items = RestaurantMenuItem.objects.filter(
            availability=True).select_related('product').select_related(
            'restaurant')
        restaurant_products = defaultdict(set)
        for item in restaurant_menu_items:
            restaurant_products[item.restaurant].add(item.product)

        products = [order_elements.product for order_elements in
                    order.elements.all()]
        available_restaurants = []
        for restaurant, menu in restaurant_products.items():
            if set(products).issubset(menu):
                available_restaurants.append(restaurant.id)
        context['adminform'].form.fields[
            'cooking_restaurant'].queryset = Restaurant.objects.filter(
            id__in=available_restaurants)

        return super().render_change_form(request, context,
                                          *args, **kwargs)


@admin.register(OrderElements)
class OrderElementsAdmin(admin.ModelAdmin):
    raw_id_fields = ("order", "product")
    list_display = ["order", "product", "quantity", "price_in_order",
                    "get_product_price"]
    readonly_fields = ["price_in_order"]

    def save_model(self, request, obj, form, change):
        obj.price_in_order = obj.product.price
        obj.save()

    def get_product_price(self, obj):
        return obj.get_product_price()

    get_product_price.short_description = 'Стоимость продукта на данный момент'
