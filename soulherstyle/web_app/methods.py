from django.shortcuts import redirect

def verifyJWT(redirect_to, token=None): 
    def wrapfunc(func): 
        def innerwrap(request, *args, **kwargs): 
            if request.COOKIES.get(token): 
                return redirect(redirect_to)
            
            return func(request, *args, **kwargs)
        return innerwrap
    return wrapfunc