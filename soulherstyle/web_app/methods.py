import jwt 
import uuid

from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import AnonymousUser

from soulherstyle.settings import SECRET_KEY, ACCOUNT_PAGE
from web_app.models import User


def set_tokens(response:HttpResponse, payload:dict, key:str, algor:str, refresh_age=None, access_age=None) -> HttpResponse: 

   access_token_id = str(uuid.uuid4())
   refresh_token_id = str(uuid.uuid4())

   payload.setdefault('accessTxnId', access_token_id)
   access_token = jwt.encode(payload=payload, key=key, algorithm=algor)

   refresh_token_payload = {'currentAccessTxnId': access_token_id, 'currentRefreshTxnId': refresh_token_id}
   refresh_token = jwt.encode(payload=refresh_token_payload, key=key, algorithm=algor)

   response.set_cookie('access_token', access_token, max_age=300 or access_age, httponly=True)
   response.set_cookie('refresh_token', refresh_token, max_age=86400 or refresh_age, httponly=True)
   
   return response



def already_authenticated(whereto=None): 
    def inner_func(func):
        def inner_wrap(request:HttpRequest, *args, **kwargs):
            if request.user.is_authenticated and request.isValid:
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
            except:
                pass
        return self.get_response(request)


class BlockJwtTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 

    def __call__(self, request:HttpRequest) -> HttpResponse: 
        refresh_token = request.COOKIES.get('refresh_token', None)
        access_token = request.COOKIES.get('access_token', None)

        if refresh_token and access_token:
            try: 
                decode_refresh_tkn = jwt.decode(refresh_token, key=SECRET_KEY, algorithms=['HS256'])
                decode_access_tkn = jwt.decode(access_token, key=SECRET_KEY, algorithms=['HS256'])

                current_token = decode_access_tkn.get('accessTxnId', None)
                currentTokenInRefresh = decode_refresh_tkn.get('currentAccessTxnId')

                if current_token == currentTokenInRefresh:
                    request.isValid = True
                    
                    current_user = User.objects.get(email=request.access_token.get('user'))
                    request.user = current_user
            except:
                pass
          
        request.isValid = False
        return self.get_response(request)



