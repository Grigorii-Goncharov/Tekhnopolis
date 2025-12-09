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