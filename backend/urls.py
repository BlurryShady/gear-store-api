from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import JsonResponse
import os
from pathlib import Path
from django.views.static import serve

def health(request):
    return JsonResponse({"status": "ok"})

def media_debug(request):
    try:
        root = Path(getattr(settings, "MEDIA_ROOT", ""))
        products_dir = root / "products"
        files = []

        if products_dir.exists():
            files = sorted([p.name for p in products_dir.iterdir() if p.is_file()])[:50]

        return JsonResponse({
            "cwd": os.getcwd(),
            "MEDIA_URL": getattr(settings, "MEDIA_URL", None),
            "MEDIA_ROOT": str(root),
            "products_dir": str(products_dir),
            "products_dir_exists": products_dir.exists(),
            "sample_files": files,
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "cwd": os.getcwd(),
            "MEDIA_URL": getattr(settings, "MEDIA_URL", None),
            "MEDIA_ROOT": str(getattr(settings, "MEDIA_ROOT", None)),
        }, status=500)

urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
    path("api/", include("store.urls")),
    path("_media_debug/", media_debug),  # remove later
]

# Serve media files (Render / portfolio demo)
urlpatterns += [
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
