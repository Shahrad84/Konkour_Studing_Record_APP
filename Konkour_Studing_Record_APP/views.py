from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home_view(request):
    """
    صفحه‌ی اصلی سایت
    """
    return render(request, "home.html")