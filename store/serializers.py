from rest_framework import serializers
from .models import Category, Brand, Product, Order, OrderItem
from django.contrib.auth import get_user_model


User = get_user_model()



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "website"]


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "brand",
            "category",
            "price",
            "stock",
            "main_image",
            "image",
            "short_description",
            "long_description",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        url = obj.get_image_url() if hasattr(obj, "get_image_url") else (getattr(obj, "main_image", "") or "")
        if not url:
            return ""
        if request:
            return request.build_absolute_uri(url)
        return url


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "brand",
            "category",
            "price",
            "stock",
            "main_image",
            "image",
            "short_description",
            "long_description",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        url = obj.get_image_url() if hasattr(obj, "get_image_url") else (getattr(obj, "main_image", "") or "")
        if not url:
            return ""
        if request:
            return request.build_absolute_uri(url)
        return url


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "status",
            "total_price",
            "created_at",
            "items",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user
