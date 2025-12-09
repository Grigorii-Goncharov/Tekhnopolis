from django.db import models
from django.core.exceptions import ValidationError


class Supplier(models.Model):
    """
    Модель поставщика в иерархической структуре торговой сети электроники.
    Поддерживает три типа поставщиков:
            - Завод (уровень 0): не имеет поставщика.
            - Розничная сеть (уровень 1 или 2): может получать товар от завода или ИП.
            - ИП (уровень 1 или 2): может получать товар от завода или другого ИП.
    Реализована валидация иерархии: максимальная глубина — 2 уровня ниже завода.
    Задолженность перед поставщиком хранится, но не может быть изменена через стандартные формы
    без дополнительной бизнес-логики (рекомендуется контролировать отдельно).
    """

    SUPPLIER_TYPES = (
        ('factory', 'Завод-изготовитель'),
        ('retail', 'Розничная сеть'),
        ('entrepreneur', 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)

    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients',
        verbose_name="Поставщик"
    )

    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    type = models.CharField(max_length=20, choices=SUPPLIER_TYPES, verbose_name="Тип поставщика")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        """
        Строковое представление вывода о поставщике
        """
        return f"{self.name} ({self.type})"

    def clean(self):
        """
        Валидация бизнес-правил иерархии поставщиков:
            - Завод не может иметь поставщика.
            - Поставщик должен находиться на один уровень выше в иерархии: завод → (розница/ИП) → (розница/ИП).
            - Глубже двух уровней от завода — запрещено.
        """
        if self.type == 'factory' and self.supplier:
            raise ValidationError("Завод не может иметь поставщика.")

        # Проверка допустимой иерархии: только до 2 уровня вложенности
        if self.supplier:
            if self.supplier.type == 'factory':
                # Уровень 1 — допустимо
                pass
            elif self.supplier.supplier and self.supplier.supplier.type == 'factory':
                # Уровень 2 — допустимо
                pass
            else:
                raise ValidationError("Поставщик должен быть на уровень выше (максимум 2 уровня от завода).")

    def get_level(self):
        """
        Возвращает уровень иерархии поставщика:
        - 0: Завод
        - 1: Прямой клиент завода
        - 2: Клиент клиента завода (второй уровень)
        """
        if self.type == 'factory':
            return 0
        elif self.supplier and self.supplier.type == 'factory':
            return 1
        else:
            return 2


class Product(models.Model):
    """
    Модель продукта, связанного с конкретным поставщиком.
    Каждый продукт имеет название, модель и дату поступления на рынок.
    Привязка к поставщику позволяет отслеживать, кто поставил товар в торговую сеть.
    При удалении поставщика все его продукты удаляются каскадно.
    """

    name = models.CharField(max_length=255, verbose_name="Название продукта")
    product_model = models.CharField(max_length=255, verbose_name="Модель продукта")
    market_release_date = models.DateField(verbose_name="Дата поступления на рынок")
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Поставщик"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        """
        Строковое представление вывода о продукте
        """
        return f"{self.name} ({self.model})"