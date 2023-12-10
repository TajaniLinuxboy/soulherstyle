from django.urls import path 

from web_app import views


urlpatterns = [
    path('register/', views.register, name='web_app-register'),
    path('register-validation/', views.register_validation, name='web_app-register-validation'),
    path('login/', views.login, name='web_app-login'), 
    path('login_validation', views.login_validation, name='web_app-login-validation'),
    path('account/', views.account, name="web_app-account"),
    path('logout', views.logout, name='web_app-logout')
]