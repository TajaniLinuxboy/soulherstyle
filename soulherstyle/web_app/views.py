import jwt

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.hashers import make_password, check_password

from web_app import forms, models
from web_app.methods import verifyJWT, replace_token

from soulherstyle.settings import SECRET_KEY


# Create your views here.
@verifyJWT('web_app-account', 'token:user')
def register(request): 
    form = forms.RegisterForm()

    response = render(request, 'web_app/register.html', context={'form': form})
    jwt_token = jwt.encode(payload={'loggedIn': 'false'}, key=SECRET_KEY, algorithm='HS256') 
    response.set_cookie('token:anonymous', jwt_token, max_age=60, httponly=True)

    return response

@verifyJWT('web_app-account', 'token:user')
def register_validation(request): 
    if request.method == "POST": 
        form = forms.RegisterForm(request.POST)

        if form.is_valid(): 
            form.save()

    error = "This email already exists"
    return HttpResponse(error)

@verifyJWT('web_app-account', 'token:user')
def login(request): 
    form = forms.LoginForm()

    if request.COOKIES.get('token'): 
        return redirect('web_app-account')

    return render(request, 'web_app/login.html', context={'form': form}) 

@verifyJWT('web_app-account', 'token:user')
def login_validation(request):
    if request.method == "POST": 
        form = forms.LoginForm(request.POST)

        if form.is_valid(): 
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try: 
                get_user = models.User.objects.get(email=email)
                if password == get_user.password: #if check_password(password, get_user.password)
                    response = redirect('web_app-account')
                    return replace_token(response, {'user': get_user.email}, key=SECRET_KEY, algro='HS256')
                
                else:
                    return HttpResponseNotFound("Invalid Password")
            except models.User.DoesNotExist as err:
                return HttpResponseNotFound("User Doesn't Exist ")


@verifyJWT('web_app-register', 'token:anonymous')
def account(request): 
       response = render(request, 'web_app/account.html')
       return response


@verifyJWT('web_app-register', 'token:anonymous')
def logout(request): 
    form = forms.RegisterForm()

    if request.method == "GET":
        response = redirect('web_app-register')
        response.delete_cookie('token:user')
        return response
