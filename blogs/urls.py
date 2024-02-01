from django.urls import path,include
from django.contrib import admin
from lxpapp import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
urlpatterns = [

    path('ushms', TemplateView.as_view(template_name='blogs/ushms.html'),name='ushms'),

]


