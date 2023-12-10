import jwt 

from django.shortcuts import redirect
from django.http import HttpResponse

def verifyJWT(redirect_to:str, token=None): 
    def wrapfunc(func): 
        def innerwrap(request, *args, **kwargs): 
            if request.COOKIES.get(token): 
                return redirect(redirect_to)
            
            return func(request, *args, **kwargs)
        return innerwrap
    return wrapfunc


def replace_token(response:HttpResponse, payload:dict, key:str, algro:str): 
    response.delete_cookie('token:anonymous')

    new_token = jwt.encode(payload=payload, key=key, algorithm=algro)
    response.set_cookie('token:user', new_token, httponly=True, max_age=60)

    return response


#def logout(response:HttpResponse, key:str, algro:str): 
#    response.delete_cookie('token:user')
#
#    anonymous_token = jwt.encode(payload={'loggedIn':'False'}, key=key, algorithm=algro)
#    response.set_cookie('token:anonymous', anonymous_token)
#
#    return response