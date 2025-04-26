from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import TemplateView
from Accounts.models import User  # Import your custom User model

# Create User View for Registration
class create_user(TemplateView):
    template_name = 'login/signup.html'  # This is where the signup form will be rendered

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2') 
        mobile_number = request.POST.get('phone')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')  # Redirect to the signup page if the email exists

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('signup')  # Redirect if passwords don't match

        # Create the user
        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
            mobile_number=mobile_number
        )

        # Log the user in after successful registration
        login(request, user)
        messages.success(request, "Registration successful")
        return redirect('home')  # Redirect to home after successful registration

# Login View
class LoginUser(TemplateView):
    template_name = 'login/login.html'
    
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
