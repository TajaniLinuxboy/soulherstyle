import jwt

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.hashers import make_password, check_password #for future use
from django.contrib.auth.decorators import login_required


from web_app import forms, models
from web_app.methods import set_tokens, already_authenticated

from soulherstyle.settings import SECRET_KEY

# Create your views here.
@already_authenticated()
def register(request): 
    form = forms.RegisterForm()
    return render(request, 'web_app/register.html', context={'form': form})

@already_authenticated()
def register_validation(request): 
    if request.method == "POST": 
        form = forms.RegisterForm(request.POST)

        if form.is_valid(): 
            form.save()

    error = "This email already exists"
    return HttpResponse(error)

@already_authenticated()
def login(request): 
    form = forms.LoginForm()
    return render(request, 'web_app/login.html', context={'form': form}) 


@already_authenticated()
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
                    payload = {'valid': True, 'user': get_user.email}
                    return set_tokens(response, payload=payload, key=SECRET_KEY, algor='HS256')
                
                else:
                    return HttpResponseNotFound("Invalid Password")
            except models.User.DoesNotExist as err:
                return HttpResponseNotFound(str(err))


@login_required(login_url='web_app-login')
def account(request): 
       response = render(request, 'web_app/account.html')
       return response


@login_required(login_url='web_app-login')
def logout(request): 
    
    if request.method == "GET":
        response = redirect('web_app-register')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


