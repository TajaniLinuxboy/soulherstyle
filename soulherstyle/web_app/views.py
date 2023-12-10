import jwt

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from web_app import forms, models

from soulherstyle.settings import SECRET_KEY


# Create your views here.
def register(request): 
    if request.COOKIES.get('token'): 
        return redirect('web_app-account')
    form = forms.RegisterForm()
    return render(request, 'web_app/register.html', context={'form': form})

def register_validation(request): 
    if request.method == "POST": 
        form = forms.RegisterForm(request.POST)

        if form.is_valid(): 
            form.save()

    error = "This email already exists"
    return HttpResponse(error)


def login(request): 
    form = forms.LoginForm()

    if request.COOKIES.get('token'): 
        return redirect('web_app-account')

    return render(request, 'web_app/login.html', context={'form': form}) 

def login_validation(request):
    if request.method == "POST": 
        form = forms.LoginForm(request.POST)

        if form.is_valid(): 
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try: 
                get_user = models.User.objects.get(email=email)
                if password == get_user.password: #if check_password(password, get_user.password)
                    return redirect('web_app-account')
                else: 
                    return HttpResponse('Invalid Email or Password') 
            except models.User.DoesNotExist as err:
                return HttpResponse(err)


def account(request): 
       response = render(request, 'web_app/account.html')
       jwt_token = jwt.encode(payload={'in': True, 'user': 'some email'}, key=SECRET_KEY, algorithm='HS256') 
       response.set_cookie('token', jwt_token, max_age=60, httponly=True)
       
       return response


def logout(request): 
    form = forms.RegisterForm()

    if request.method == "GET": 
        response = render(request, 'web_app/register.html', context={'form': form})
        response.delete_cookie('token')

        return response