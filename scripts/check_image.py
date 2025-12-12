import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.test import RequestFactory
from store.models import Product
from store.serializers import ProductDetailSerializer

host = os.getenv("CHECK_HOST", "127.0.0.1:8000")

rf = RequestFactory()
request = rf.get("/", HTTP_HOST=host)

p = Product.objects.first()
print("product:", p.slug, "image_file.name=", p.image_file.name)

serializer = ProductDetailSerializer(p, context={"request": request})
print("serialized image:", serializer.data.get("image"))
