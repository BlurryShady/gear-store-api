from django.contrib import admin
from .models import Category, Brand, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "website")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "price", "stock", "is_active")
    list_filter = ("brand", "category", "is_active")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_email", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_email")
    inlines = [OrderItemInline]