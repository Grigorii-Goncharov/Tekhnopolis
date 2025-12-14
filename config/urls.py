# config/urls.py

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.root_redirect, name="home"),
    path("users/", include("users.urls")),
    path("store/", include("store.urls")),
    # Маршруты для drf_spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
