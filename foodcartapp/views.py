from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from banners.models import Slug
from .models import Product, Order, OrderElements
from .serializers import OrderSerializer, OrderDeleteSerializer, \
    OrderUpdateSerializer


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


def create_order(serializer: OrderSerializer) -> Response:
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


def delete_order(serializer: OrderDeleteSerializer) -> Response:
    order = get_object_or_404(Order, id=serializer.validated_data["id"])
    serialize_order = OrderSerializer(order)
    order.delete()
    return Response(serialize_order.data)


def update_order(serializer: OrderUpdateSerializer) -> Response:
    order = get_object_or_404(Order, id=serializer.validated_data["id"])
    firstname = serializer.validated_data.get('firstname')
    if firstname:
        order.firstname = firstname
    lastname = serializer.validated_data.get('lastname')
    if lastname:
        order.lastname = lastname
    phonenumber = serializer.validated_data.get('phonenumber')
    if phonenumber:
        order.phonenumber = phonenumber
    address = serializer.validated_data.get('address')
    if address:
        order.address = address
    order.save()

    serialize_order = OrderSerializer(order)
    return Response(serialize_order.data)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
@api_view(['POST', 'PATCH', 'DELETE'])
def register_order(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return create_order(serializer)
    if request.method == 'DELETE':
        serializer = OrderDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return delete_order(serializer)
    if request.method == 'PATCH':
        serializer = OrderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return update_order(serializer)
