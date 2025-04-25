from django.http import HttpRequest

def home(request):
    return HttpRequest("home page")