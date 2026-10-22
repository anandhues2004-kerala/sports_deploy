from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Customer





# Create your views here.

def sign_up(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Required field validation
        if not all([
            username,
            email,
            phone,
            address,
            password,
            confirm_password
        ]):
            error_message = "All fields are required"

        # Password validation
        elif password != confirm_password:
            error_message = "Passwords do not match"

        # Username validation
        elif User.objects.filter(username=username).exists():
            error_message = "Username already exists"

        # Email validation
        elif User.objects.filter(email=email).exists():
            error_message = "Email already exists"

        else:
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                customer=Customer.objects.create(
                    name=username,
                    user=user,
                    phone=phone,
                    address=address
                )

                # Save extra information
                # Phone and address need a separate model/profile
                # if you want to store them.

                return redirect("login")

            except Exception as e:
                error_message = "Something went wrong"

    return render(
        request,
        "register.html",
        {"error_message": error_message}
    )

def user_login(request):
    error_message=None
    if request.POST:
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return  redirect("index")
        else:
            error_message="invalid user Name and Password"
    return render(request,"login.html",{"error_message":error_message})  

def user_logout(request):
     logout(request)
     return redirect("index") 

#################################################################
def about(request):
    return render(request,"about.html")

def return_policy(request):
    return render(request, "return.html")

def blog_view(request):
    return render(request,"blog.html")
            
