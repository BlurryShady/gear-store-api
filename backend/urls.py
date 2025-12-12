from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
    path("api/", include("store.urls")),
]
if settings.DEBUG or os.environ.get("SERVE_MEDIA") == "1":
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )