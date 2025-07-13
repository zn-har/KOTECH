"""
URL configuration for KOTECH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    # path('', include('Accounts.urls')),
    path('',views.HomeView.as_view(), name='home'),
    path('register/ideathon', views.IdeathonRegistrationView.as_view(), name='Ideathon'),
    path('register/ideathon/', views.IdeathonRegistrationView.as_view(), name='Ideathon'),
    
    path('register/hackathon/', views.HackathonRegistrationView.as_view(), name='hackathon_registration'),
    path('register/hackathon', views.HackathonRegistrationView.as_view(), name='hackathon_registration'),
    path('register/readmission', views.ReadmissionView.as_view(), name='readmission'),
        
    
    path('register/media/', views.MediaRegisterView.as_view(), name='media'),
    path('register/project_exhibition/', views.ExpoRegisterView.as_view(), name='register'),
    path('register/project_exhibition', views.ExpoRegisterView.as_view(), name='register'),
    path('registration_success', views.registration_success, name="registration_success"),
    # re_path(r'^.*$', views.under_construction, name='under_construction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


