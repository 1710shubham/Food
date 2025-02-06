from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
import re
from .models import Admin
from django.core.files.storage import FileSystemStorage
from django_ratelimit.decorators import ratelimit

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
                request.session['Role'] = user.Role
                if user.Role == 0:
                 return redirect('index')
                elif user.Role == 2:
                    return redirect('dash')
            else:
                message = "Password Doesn't match"
                return render(request,"app/login.html",{'msg':message})
        except User.DoesNotExist:
             email_msg = "User doesn't exist"
             return render(request, "app/login.html", {'email_msg': email_msg})




def RegisterPage(request):
    return render(request,"app/register.html")

def Index(request):
    if 'Name' not in request.session:
        return redirect('loginpage')
    name=request.session.get('Name','')
    food_items = Admin.objects.all().order_by('?')[:6]
    return render(request, "app/index.html", {'name': name, 'food_items': food_items})

def LogoutUser(request):
    request.session.flush()
    return redirect('loginpage')

def Menu(request):
    if 'Name' not in request.session:
        return redirect('loginpage')
    food_items = Admin.objects.all()
    return render(request,"app/menu.html",{'food_items':food_items})

def About(request):
    if 'Name' not in request.session:
        return redirect('loginpage')
    return render(request,"app/about.html")

def Dash(request):
     if 'Name' not in request.session:
        return redirect('loginpage')
     total_users = User.objects.filter(Role=0).count()
     name = request.session.get('Name', '')
     return render(request, "app/dash.html", {'name': name,'total_users':total_users})



#====ADMIN SIDE======#

def AdminOrder(request):
    if request.method == "POST":
        food_name = request.POST['food_name']
        food_description = request.POST['food_description']
        food_price = request.POST['food_price']
        food_category = request.POST['food_category']
        food_image = request.FILES['food_image']  # Handle file upload
        
        # Save the food item to the database
        new_food_item = Admin.objects.create(
            Food_Name=food_name,
            Food_Description=food_description,
            Food_Price=food_price,
            Food_Category=food_category,
            Food_Image=food_image  # The image will be automatically saved in MEDIA_ROOT/food_images/
        )
        return render(request, "app/form_admin.html", {'messages': 'Food Item Added Successfully!'})

    return render(request, "app/form_admin.html")


def FormAdmin(request):
    food_items = Admin.objects.all()
    return render(request, "app/form_admin.html",{'food_items':food_items})

def EditAdmin(request, food_id):
    food = get_object_or_404(Admin, id=food_id)
    return render(request, "app/edit_admin.html", {'food': food})

def Update(request,id):
    food = get_object_or_404(Admin, id=id)
    if request.method == "POST":
        food_name = request.POST['food_name']
        food_description = request.POST['food_description']
        food_price = request.POST['food_price']
        food_category = request.POST['food_category']
        food_image = request.FILES['food_image']  # Handle file upload
        
        # Save the food item to the database
        food.Food_Name = food_name
        food.Food_Description = food_description
        food.Food_Price = food_price
        food.Food_Category = food_category

        # Only update the image if a new one was uploaded
        if food_image:
            food.Food_Image = food_image  # Save the new image

        food.save() 
        return render(request,"app/form_admin.html",{'messages': 'Food Item Updated Successfully!'})
#====ADMIN SIDE======#
