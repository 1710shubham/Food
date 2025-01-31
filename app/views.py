from django.shortcuts import render
from .models import *
from django.http import HttpResponse


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

        user = User.objects.filter(Email=email).first()

        if user:
            message = "User Already Exists"
            return render(request,"app/register.html",{'msg':message})
        else:
            if password == cpassword:
                new_user = User.objects.create(
                    Name = name,
                    Email = email,
                    Contact = contact,
                    Password=password
                )
                return render(request,"app/login.html")
            else:
                message = "Password and Confirm Password Doesn't match"
                return render(request,"app/register.html",{'msg':message})
            


def RegisterPage(request):
    return render(request,"app/register.html")
