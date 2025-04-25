from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot/', views.forgot, name='forgot'),
]
