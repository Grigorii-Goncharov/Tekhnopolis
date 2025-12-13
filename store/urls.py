# store/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet, supplier_list_view, product_list_view,
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('api/', include(router.urls)), # API маршруты
    path('suppliers/', supplier_list_view, name='supplier-list'),
    path('products/', product_list_view, name='product-list'),
]
