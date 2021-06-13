"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url

from django.urls import path,re_path

from . import views

from django.views.generic import RedirectView

urlpatterns = [
    re_path(r'^$',views.index),
    path('index/',views.index),
    path('DH/', views.DH),
    path('AES/', views.AES),
    path('RSA/', views.RSA),
    path('LFSR_JK/', views.LFSR_JK),
    path('Affine/', views.Affine),
    path('404/', views.notfound_404),
    path('DES/', views.DES),
    path('RC4/', views.RC4),
]
