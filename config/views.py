# config/views.py
from django.shortcuts import redirect

def root_redirect(request):
    """
    Представление для перенаправления корня сайта (/) на страницу входа.
    """
    return redirect('users:login')