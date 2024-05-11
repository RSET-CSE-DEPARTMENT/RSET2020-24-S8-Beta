"""detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.first),
    path('index',views.index),
    path('register',views.register),
    path('registration',views.registration),
    path('login/',views.login),
    path('login/addlogin',views.addlogin),
    path('logout/',views.logout),
    path('v_users',views.v_users),
    path('test',views.test),
    path('addfile',views.addfile),
    path('v_result',views.v_result),
    path('v_results',views.v_results),
    path('download_generated_dance',views.download_generated_dance,name="download_generated_dance"),
    path('live',views.live),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
