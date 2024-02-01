from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

def activate(request, uidb64, token):

    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    usertoken = User.objects.raw('SELECT user_id as id, activation_token FROM auth_userprofile WHERE user_id = ' + str(uidb64))
    for x in usertoken:
        usertoken = x.activation_token
    
    if user is not None and usertoken is not None and usertoken == token:
        user.is_active = True
        user.save()
        usertoken = User.objects.raw('UPDATE social_auth_usersocialauth SET utype = 1 WHERE user_id = ' + str(uidb64))
        return render(request, 'lxpapp/index.html')
    
    else:
        # Display an error page
        return render(request, 'lxpapp/users/activation_error.html')
