from django.urls import path

from .views import product_list_api, banners_list_api, register_order, \
    get_banner

app_name = "foodcartapp"

urlpatterns = [
    path('banner/<slug:slug_title>', get_banner, name='banner'),
    path('products/', product_list_api),
    path('banners/', banners_list_api),
    path('order/', register_order),
]
