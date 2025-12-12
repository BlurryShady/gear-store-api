from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        "products": "/api/products/",
        "categories": "/api/categories/",
        "brands": "/api/brands/",
        "auth": {
            "register": "/api/auth/register/",
            "login": "/api/auth/login/",
            "token": "/api/auth/token/",
            "refresh": "/api/auth/token/refresh/",
        }
    })



urlpatterns = [

    path("", api_root),
    #Products, Categories and Brands
    path("categories/", views.category_list, name="category-list"),
    path("brands/", views.brand_list, name="brand-list"),
    path("products/", views.product_list, name="product-list"),
    path("products/<slug:slug>/", views.product_detail, name="product-detail"),

    #Orders
     path("orders/", views.order_list_create, name="order-list-create"),
     path("orders/my/", views.my_orders, name="my-orders"),

    #Path
    path("auth/register/", views.register, name="register"),
    path("auth/me/", views.me, name="me"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

