from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Supplier, Product
from .serializers import SupplierCreateUpdateSerializer, SupplierSerializer


def home(request):
    # Это для API
    from django.http import JsonResponse
    return JsonResponse({"message": "Добро пожаловать в API сети электроники!"})


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    # serializer_class = SupplierSerializer # Будет выбран динамически
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']
    search_fields = ['city'] # Поиск по городу

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            # Для создания и обновления используем сериализатор без поля debt
            return SupplierCreateUpdateSerializer
        # Для всех остальных действий (list, retrieve) используем полный сериализатор
        return SupplierSerializer

# --- Обновлённая функция для главной страницы ---
# def welcome_view(request):
#     """Главная страница приветствия."""
#     # Теперь эта страница всегда доступна всем, включая неавторизованных пользователей
#     # Можно передавать информацию о пользователе в шаблон
#     return render(request, 'store/welcome.html', {'user': request.user})

def login_view(request):
    """Страница входа в систему."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            # Перенаправляем после успешного входа, например, на список поставщиков
            return redirect('supplier-list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    # Если GET запрос или ошибка, просто отображаем форму
    return render(request, 'store/login.html')

@login_required
def supplier_list_view(request):
    """Отображает список всех поставщиков."""
    suppliers = Supplier.objects.all()
    return render(request, 'store/supplier_list.html', {'suppliers': suppliers})

@login_required
def product_list_view(request):
    """Отображает список всех продуктов."""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})
