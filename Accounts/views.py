from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import TemplateView
from Accounts.models import User
import captcha
import requests
from django.conf import settings




# Create User View for Registration

class RegisterUser(TemplateView):
    template_name = 'login/signup.html'  # Your template file
    def get (self, request, *args, **kwargs):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile_number = request.POST.get('mobile_number')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify reCAPTCHA
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect('signup')
        

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
            mobile_number=mobile_number
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login') # Redirect to home after successful registration

# Login View
class LoginUser(TemplateView):
    template_name = 'login/login.html'

    def get(self, request):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
    
    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Authenticate the user based on email and password
        user = authenticate(request, email=email, password=password)
        
        # If authentication is successful, log the user in
        if user is not None:
            login(request, user)
            return redirect('/admin/')  # Redirect to home or any other page after successful login
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login/login.html')  # Show the login form again if authentication fails


class Signup(TemplateView):
    template_name = 'login/signup.html'

class Forgot(TemplateView):
    template_name = 'login/forgot.html'
