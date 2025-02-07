from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
import re
from .models import Admin
from .models import User
from .forms import OrderForm
# from django.core.files.storage import FileSystemStorage
# from django_ratelimit.decorators import ratelimit



# Create your views here.
def place_order(request, food_id):
    food_item = get_object_or_404(Admin, id=food_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Get the currently logged-in user
            user = request.user  # Assuming the user is authenticated
            form.save(user=user)  # Save the order with the user information
            return redirect('order_success')  # Redirect to a success page

    else:
        form = OrderForm(initial={'food_item': food_item})  # Pre-fill the food item

    return render(request, "app/order.html", {'form': form, 'food_item': food_item})

def order_success(request):
    return render(request, "app/order_success.html")





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

        user = User.objects.filter(email=email).first()

        if user:
            email_msg = "User Already Exists"
            return render(request,"app/register.html",{'email_msg':email_msg})
        else:
            if password == cpassword:
                hashed_password =make_password(password)
                new_user = User.objects.create(
                    name = name,
                    email = email,
                    contact = contact,
                    password=hashed_password
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
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['name'] = user.name
                request.session['email'] = user.email
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
    if 'name' not in request.session:
        return redirect('loginpage')
    name=request.session.get('name','')
    food_items = Admin.objects.all().order_by('?')[:6]
    return render(request, "app/index.html", {'name': name, 'food_items': food_items})

def LogoutUser(request):
    request.session.flush()
    return redirect('loginpage')

def Menu(request):
    if 'name' not in request.session:
        return redirect('loginpage')
    food_items = Admin.objects.all()
    return render(request,"app/menu.html",{'food_items':food_items})

def About(request):
    if 'name' not in request.session:
        return redirect('loginpage')
    return render(request,"app/about.html")

def Dash(request):
     if 'name' not in request.session:
        return redirect('loginpage')
     total_users = User.objects.filter(Role=0).count()
     name = request.session.get('name', '')
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


def Delete(request, id):
    # Fetch the existing food item by id
    food = get_object_or_404(Admin, id=id)
    
    # Delete the food item
    food.delete()
    
    # After deletion, redirect to another page (for example, a list page)
    return render(request,"app/form_admin.html",{'messages': 'Food Item Deleted Successfully!'})

#====ADMIN SIDE======#

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import password_validation

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            reset_url = f"{get_current_site(request).domain}/reset-password/{uid}/{token}/"

            subject = "Password Reset Request"
            message = f"Click the link to reset your password: {reset_url}"
            send_mail(subject, message, 'skmalani05@gmail.com', [email])

            return HttpResponse("A password reset link has been sent to your email.")
        else:
            return HttpResponse("User with this email does not exist.")
    return render(request, "app/password_reset_request.html")





from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')

            # Validate password strength
            try:
                password_validation.validate_password(new_password, user)
            except Exception as e:
                return HttpResponse(f"Password validation error: {str(e)}")

            # Update the password
            user.password = make_password(new_password)
            user.save()

            return redirect('loginpage')
        return render(request, "app/password_reset_confirm.html")
    else:
        return HttpResponse("The link is invalid or has expired.")

