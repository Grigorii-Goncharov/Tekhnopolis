# config/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny # Импортируем разрешение
from . import views

# Создаём кастомное представление для схемы с открытым доступом
class PublicSchemaView(SpectacularAPIView):
    permission_classes = [AllowAny] # Открываем доступ

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.root_redirect, name="home"),
    path("users/", include("users.urls")),
    path("store/", include("store.urls")),
    # Маршруты для drf_spectacular
    # Используем кастомное представление для схемы
    path("api/schema/", PublicSchemaView.as_view(), name="schema"), # <-- Изменено
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
