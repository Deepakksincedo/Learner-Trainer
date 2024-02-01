# from lxpapp import models as mod
# from django.utils import timezone
# class UserActivityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             from datetime import datetime
#             import pytz
#             tz = pytz.timezone('Asia/Kolkata')
#             current_time = datetime.now(tz)
#             path = str( request.path)
#             # if(path.startswith("/indexpage") 
#             #    or path.startswith("/cto") 
#             #    or path.startswith("/cfo") 
#             #    or path.startswith("/trainer") 
#             #    or path.startswith("/learner") 
#             #    or path.startswith("/admin") 
#             #    or path.startswith("/signup") 
#             #    or path.startswith("/login") 
#             #    or path.startswith("/logout") 
#             #    or path.startswith("/social-auth") 
#             #    or path.startswith("/aboutus") 
#             #    or path.startswith("/contactus") 
#             #    or path.startswith("/indexpage") 
#             #    or path.startswith("/user-session-expired") 
#             #    or path.startswith("/userlogin") 
#             #    or path.startswith("/update-user") 
#             #    or path.startswith("/active-user") 
#             #    or path.startswith("/inactive-user") 
#             #    or path.startswith("/delete-user") 
#             #    or path.startswith("/register") 
#             #    or path.startswith("/user-change-password") 
#             #    or path.startswith("/termsandconditions") 
#             #    or path.startswith("/privacypolicy") 
#             #    or path.startswith("/ushms")): 
#             #     mod.UserActivity.objects.create(user=request.user, url=path,timestamp = current_time)
#             mod.UserActivity.objects.create(user=request.user, url=path,timestamp = current_time)
#         response = self.get_response(request)
#         return response

import logging
import threading
import traceback

from lxpapp.models import UserActivity, ErrorLog


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals = threading.local()
        thread_locals.request = request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_request():
        return getattr(threading.local(), 'request', None)


class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception('An error occurred during view processing')
            ErrorLog.objects.create(
                user=request.user,
                url=request.path,
                exception=str(e),
                traceback=traceback.format_exc()
            )
            raise e
        return response


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception('An error occurred during view processing')
            ErrorLog.objects.create(
                user=request.user,
                url=request.path,
                exception=str(e),
                traceback=traceback.format_exc()
            )
            raise e
        if request.user.is_authenticated and not request.path.__contains__('email-decode.min.js') and request.path != '/':
            UserActivity.objects.create(
                user=request.user,
                url=request.path,
                method=request.method,
                status_code=response.status_code if response else None
            )
        return response
