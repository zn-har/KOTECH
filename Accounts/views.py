from django.shortcuts import render

def login(request):
    return render(request,'login/login.html')
def signup(request):
    return render(request, 'login/signup.html')
# Create your views here.