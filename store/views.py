from decimal import Decimal
from django.db import transaction
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Brand, Product, Order, OrderItem
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    OrderSerializer,
    UserSerializer,
    RegisterSerializer,
)

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


User = get_user_model()


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def brand_list(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_list(request):
    products = Product.objects.filter(is_active=True)

    # Read query parameters
    category_id = request.query_params.get("category")
    brand_id = request.query_params.get("brand")
    search = request.query_params.get("search")
    ordering = request.query_params.get("ordering")

    if category_id:
        products = products.filter(category_id=category_id)

    if brand_id:
        products = products.filter(brand_id=brand_id)

    if search:
        products = products.filter(
            Q(name__icontains=search)
            | Q(short_description__icontains=search)
            | Q(long_description__icontains=search)
        )

    # Only allow safe ordering fields
    if ordering in ["price", "-price", "created_at", "-created_at"]:
        products = products.order_by(ordering)

    # Pagination
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(products, request)

    if page is not None:
        serializer = ProductListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    # Fallback (in case pagination is disabled)
    serializer = ProductListSerializer(products, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug, is_active=True)
    except Product.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductDetailSerializer(product, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "POST"])
def order_list_create(request):
    if request.method == "GET":
        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    # POST: create new order
    data = request.data
    items_data = data.get("items", [])

    if not items_data:
        return Response(
            {"detail": "No items provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    customer_name = data.get("customer_name", "")
    customer_email = data.get("customer_email", "")

    with transaction.atomic():
        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            customer_name=customer_name,
            customer_email=customer_email,
            status="pending",
            total_price=0,
        )

        total = Decimal("0.00")

        for item in items_data:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 0)

            if not product_id or quantity <= 0:
                transaction.set_rollback(True)
                return Response(
                    {"detail": "Invalid item data."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                transaction.set_rollback(True)
                return Response(
                    {"detail": f"Product with id {product_id} not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if product.stock < quantity:
                transaction.set_rollback(True)
                return Response(
                    {"detail": f"Not enough stock for {product.name}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            unit_price = product.price
            line_total = unit_price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
            )

            product.stock -= quantity
            product.save()

            total += line_total

        order.total_price = total
        order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
