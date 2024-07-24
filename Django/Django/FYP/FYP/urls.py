"""
URL configuration for FYP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from FYP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginPage, name="login"),
    path('logout/', views.logout, name="logout"),
    path('home/', views.Home, name="home"),
    path('display/', views.Display, name="display"),
    path('video_feed/',views.video_feed, name='video_feed'),
    path('license_check/', views.license_check, name='license_check'),
    path('search_records/', views.search_records, name='search_records'),
    path('loading/', views.loading, name="loading"), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
