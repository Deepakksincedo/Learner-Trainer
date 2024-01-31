"""
URL configuration for lntdjango project.

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
from django.contrib import admin
from django.urls import path
from  lntdjango import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.homePage),
    path('send_otp',views.send_otp),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('register',views.register,name='register_page'),
    path('add-another',views.add_another,name='ifAddingquestion'),
    path('show-answer',views.show_answers,name='showing_answer'),
    path('submit-question',views.submit,name='submit_question'),

]
