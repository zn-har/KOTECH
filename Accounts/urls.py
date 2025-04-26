from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot/', views.forgot, name='forgot'),
]
