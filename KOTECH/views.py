from django.http import HttpRequest
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')