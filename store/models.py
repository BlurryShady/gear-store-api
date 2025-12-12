from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image
import io


def validate_image_file(file_obj):
    """Validate uploaded image: size and that Pillow can open it.

    Works for files uploaded via admin or API. Raises ValidationError on failure.
    """
    # file_obj may be an InMemoryUploadedFile or FieldFile
    try:
        size = file_obj.size
    except Exception:
        size = None

    max_size = getattr(settings, "MAX_UPLOAD_SIZE", 2 * 1024 * 1024)
    if size and size > max_size:
        raise ValidationError(f"Image is too large (>{max_size} bytes)")

    # Verify image is valid
    try:
        # Pillow needs a file-like object - ensure start at beginning
        file_obj.seek(0)
        img = Image.open(file_obj)
        img.verify()
        file_obj.seek(0)
    except Exception:
        raise ValidationError("Uploaded file is not a valid image")

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 9999.99 max
    stock = models.PositiveIntegerField(default=0)

    main_image = models.URLField(blank=True)  # later I can switch to ImageField if I want

    short_description = models.CharField(max_length=255, blank=True)
    long_description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image_file = models.ImageField(
        upload_to="products/", blank=True, null=True, validators=[validate_image_file]
    )

    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        if self.main_image:
            return self.main_image
        return ""

    def __str__(self):
        return self.name
    

    

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    customer_name = models.CharField(max_length=200, blank=True)
    customer_email = models.EmailField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
