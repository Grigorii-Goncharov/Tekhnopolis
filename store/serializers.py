from rest_framework import serializers
from .models import Supplier, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ('debt', 'created_at')

    def validate(self, data):
        # Повторяем валидацию из модели
        instance = Supplier(**data)
        # Исключаем поля, которые не могут быть установлены через API
        instance.full_clean(exclude=['debt', 'created_at'])
        return data
