from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderElements


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


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


@api_view(['POST'])
def register_order(request):
    frontend_order = request.data
    try:
        products = frontend_order["products"]
    except KeyError:
        content = {"products": "Обязательное поле"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(products, str):
        content = {
            "products": "Ожидался list со значениями, но был получен 'str'"
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if products is None:
        content = {
            "products": "Это поле не может быть пустым"
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if not products:
        content = {"products": "Этот список не может быть пустым"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    order = Order.objects.create(
        first_name=frontend_order.get("firstname"),
        last_name=frontend_order.get("lastname"),
        phone_number=frontend_order.get("phonenumber"),
        address=frontend_order.get("address")
    )
    for element in frontend_order.get("products"):
        product_id, quantity = element.values()
        OrderElements.objects.create(
            order=order,
            product=get_object_or_404(Product, id=product_id),
            quantity=quantity
        )
    return Response({})
