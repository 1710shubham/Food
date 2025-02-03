from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
import re
# Create your views here.






def LoginPage(request):
    return render(request,"app/login.html")

def UserRegister(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        special_char_pattern = re.compile('[@$!%*?&]')         
        if len(password) < 8:
            password_msg = "Password must be at least 8 characters long."
            return render(request,"app/register.html",{'p_m':password_msg})
        
        if not special_char_pattern.search(password):
            password_msg = "Password must contain at least one special character (@, $, !, %, *, ?, &)."
            return render(request,"app/register.html",{'p_m':password_msg})

        user = User.objects.filter(Email=email).first()

        if user:
            email_msg = "User Already Exists"
            return render(request,"app/register.html",{'email_msg':email_msg})
        else:
            if password == cpassword:
                hashed_password =make_password(password)
                new_user = User.objects.create(
                    Name = name,
                    Email = email,
                    Contact = contact,
                    Password=hashed_password
                )
                return render(request,"app/login.html")
            else:
                message = "Password and Confirm Password Doesn't match"
                return render(request,"app/register.html",{'msg':message})
            
def LoginUser(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(Email=email)
            if check_password(password, user.Password):
                request.session['Name'] = user.Name
                request.session['Email'] = user.Email
                return render(request, "app/index.html")
            else:
                message = "Password Doesn't match"
                return render(request,"app/login.html",{'msg':message})
        except User.DoesNotExist:
             email_msg = "User doesn't exist"
             return render(request, "app/login.html", {'email_msg': email_msg})




def RegisterPage(request):
    return render(request,"app/register.html")

def Index(request):
    return render(request,"app/index.html")



