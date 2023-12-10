from typing import Any
import jwt 

from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest

from soulherstyle.settings import SECRET_KEY, ACCOUNT_PAGE
from web_app.models import User

def set_access_token(response:HttpResponse, payload:dict, key:str, algro:str) -> HttpResponse:
    access_token = jwt.encode(payload=payload, key=key, algorithm=algro)
    response.set_cookie('access_token', access_token, max_age=1000, httponly=True)

    return response


def already_authenticated(whereto=None): 
    def inner_func(func):
        def inner_wrap(request:HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(whereto or ACCOUNT_PAGE)
            
            return func(request, *args, **kwargs)
        return inner_wrap
    return inner_func


class VerifyJwtTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request:HttpRequest) -> HttpResponse: 
        access_token =  request.COOKIES.get('access_token', None)
        if access_token:
            try:
                decoded_token = jwt.decode(access_token, key=SECRET_KEY, algorithms=['HS256'])
                request.access_token = decoded_token
            except jwt.InvalidSignatureError: 
                request.COOKIES['access_token'] = None
    
        return self.get_response(request)

class JwtSetUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request:HttpRequest) -> HttpResponse:
        access_token = request.COOKIES.get('access_token', None)
        if access_token: 
            current_user = User.objects.get(email=request.access_token.get('user'))
            request.user = current_user

        return self.get_response(request)

