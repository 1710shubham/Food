from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.LoginPage,name="loginpage"),
    path("register/",views.RegisterPage,name="register"),
    path("auth_regi/",views.UserRegister,name="auth_regi"),
    path("auth_log/",views.LoginUser,name="auth_log"),
    path("index/",views.Index,name="index"),
]
