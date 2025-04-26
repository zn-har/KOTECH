from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.views.generic import TemplateView


class login_user(TemplateView):
    template_name = 'login/login.html'
    
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/admin/')  # or reverse('admin:index')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login/login.html')


def signup(request):
    return render(request, 'login/signup.html')

def forgot(request):
    return render(request, 'login/forgot.html')
