from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def health(request):
    return JsonResponse({"status": "ok"})

def media_debug(request):
    root = Path(settings.MEDIA_ROOT)
    products_dir = root / "products"
    files = []
    if products_dir.exists():
        files = sorted([p.name for p in products_dir.iterdir() if p.is_file()])[:50]
    return JsonResponse({
        "MEDIA_ROOT": str(root),
        "products_dir_exists": products_dir.exists(),
        "sample_files": files,
        "cwd": os.getcwd(),
    })

urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
    path("api/", include("store.urls")),
    path("_media_debug/", media_debug),
]
if settings.DEBUG or os.environ.get("SERVE_MEDIA") == "1":
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )