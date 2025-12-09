from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Supplier, Product

@admin.action(description="Очистить задолженность")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0.00)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'debt', 'supplier_link')
    list_filter = ('city', 'country')
    actions = [clear_debt]
    readonly_fields = ('created_at',)

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/electronics/supplier/{obj.supplier.id}/change/"
            return f'<a href="{url}">{obj.supplier.name}</a>'
        return "-"
    supplier_link.allow_tags = True
    supplier_link.short_description = "Поставщик"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'market_release_date', 'supplier')
    list_filter = ('supplier__country',)