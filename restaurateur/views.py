import requests
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.db.models import ExpressionWrapper, DecimalField
from django.db.models import Sum, F
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from geopy import distance

from foodcartapp.models import Product, Restaurant, Order
from star_burger import settings


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:
        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in
               product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in
                                restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection'][
        'featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_addresses_coordinates(addresses: list) -> dict:
    addresses_coordinates = {}
    for address in addresses:
        try:
            lon, lat = fetch_coordinates(settings.YANDEX_GEO_API_TOKEN,
                                         address)
        except TypeError:
            continue
        addresses_coordinates[address] = (lat, lon)
    return addresses_coordinates


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.unprocessed().annotate(
        total_price=Sum(
            ExpressionWrapper(
                F('order_elements__quantity') * F(
                    'order_elements__product__price'),
                output_field=DecimalField()
            )
        )
    ).get_available_restaurants()
    orders_coordinates = get_addresses_coordinates(
        [order.address for order in orders]
    )
    restaurants_coordinates = get_addresses_coordinates(
        Restaurant.objects.values_list('address', flat=True))
    for order in orders:
        order_coordinates = orders_coordinates.get(order.address)
        if not order_coordinates:
            continue
        order.distances = {}
        for restaurant in order.restaurants:
            restaurant_coordinates = restaurants_coordinates[
                restaurant.address]
            restaurant.distance = round(
                distance.distance(order_coordinates,
                                  restaurant_coordinates).km, 3)
            order.distances[restaurant] = restaurant.distance

        order.distances = sorted(order.distances.items(),
                                 key=lambda item: item[1])
        order.distances = {rest: dist for rest, dist in
                           order.distances}
    return render(request, template_name='order_items.html', context={
        'order_items': orders,
    })
