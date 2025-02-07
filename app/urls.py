from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.LoginPage,name="loginpage"),
    path("register/",views.RegisterPage,name="register"),
    path("auth_regi/",views.UserRegister,name="auth_regi"),
    path("auth_log/",views.LoginUser,name="auth_log"),
    path("index/",views.Index,name="index"),
    path("logout/", views.LogoutUser, name="logout"),
    path("menu/", views.Menu, name="menu"),
    path("about/", views.About, name="about"),
    path("dash/", views.Dash, name="dash"),
    path('admin_order/', views.AdminOrder, name='admin_order'),
    path('form_admin/', views.FormAdmin, name='form_admin'),
    path('edit_admin/<int:food_id>/', views.EditAdmin, name='edit_admin'),
    path('update/<int:id>/',views.Update,name='update'),    
    path('delete/<int:id>/',views.Delete,name='delete'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('place_order/<int:food_id>/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)