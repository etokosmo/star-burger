from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from banners.models import Banner, Slug
from .models import Product, Order, OrderElements


class OrderElementsSerializer(ModelSerializer):
    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True,
                                       allow_empty=False,
                                       write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address',
                  'products']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update(**validated_data)


def get_banner(request, slug_title):
    slug = Slug.objects.prefetch_related("banners").get(slug_title=slug_title)
    dumped_banners = []
    banners = slug.banners.all()
    for banner in banners:
        dumped_banner = {
            'title': banner.title,
            'src': banner.image.url,
            'text': banner.text,
        }
        dumped_banners.append(dumped_banner)
    return JsonResponse(
        dumped_banners,
        safe=False,
        json_dumps_params={'ensure_ascii': False}
    )


def banners_list_api(request):
    return HttpResponseRedirect(
        reverse('foodcartapp:banner',
                kwargs={'slug_title': 'start-page-header'}))


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
        address=serializer.validated_data['address']
    )

    for element in serializer.validated_data['products']:
        product, quantity = element.values()
        OrderElements.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price_in_order=product.price
        )
    serialize_order = OrderSerializer(order)
    return Response(serialize_order.data)
