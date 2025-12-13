# store/admin.py

from django.contrib import admin
from .models import Supplier, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_model', 'market_release_date', 'supplier')
    list_filter = ('supplier__city', 'supplier__country')


class ClearDebtActionMixin:
    """
    Миксин для добавления действия очистки задолженности.
    """
    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt=0.00)
        self.message_user(
            request,
            f"Задолженность была очищена у {updated_count} поставщиков."
        )

    clear_debt.short_description = "Очистить задолженность у выбранных поставщиков"


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin, ClearDebtActionMixin):
    list_display = ('name', 'type', 'get_level', 'email', 'city', 'country', 'debt', 'supplier_link')
    list_filter = ('city', 'country')
    actions = ['clear_debt']

    def supplier_link(self, obj):
        """
        Отображает ссылку на поставщика.
        """
        if obj.supplier:
            # Используем URL, который генерируется Django Admin для редактирования объекта
            url = f"/admin/store/supplier/{obj.supplier.id}/change/"
            return f'<a href="{url}">{obj.supplier}</a>'
        return '-'

    supplier_link.short_description = "Поставщик"
