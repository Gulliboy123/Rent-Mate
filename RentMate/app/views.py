from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PropertyDetail, PropertyImage
from .models import ContactUs
from .models import AboutUs
import re
from django.db.models import Q
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from RentMate.settings import EMAIL_HOST_USER
#email validation
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.conf import settings

User = get_user_model() 


# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    properties = PropertyDetail.objects.filter(approval_status='approved')
    return render(request, 'home.html', {'properties':properties})


#SIGNUP PAGE LOGIC
def SignupPage(request):
    errors = {}
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        role = request.POST.get('role')  # Get the selected role from the form

        # Validate the form fields
        if not firstname:
            errors['firstname'] = "First Name is required."
        if not lastname:
            errors['lastname'] = "Last Name is required."
        if not email:
            errors['email'] = "Email is required."
        elif '@gmail.com' not in email:
            errors['email'] = "Email must be a valid Gmail address."
        elif User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists. Please choose a different one."

        if not username:
            errors['username'] = "Username is required."
        elif len(username) < 4:
            errors['username'] = "Username must be at least 4 characters long."

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not password:
            errors['password'] = "Password is required."
        elif not re.match(password_pattern, password):
            errors['password'] = "Password must contain at least 8 characters, one uppercase, lowercase, number, and special character."

        if not confirmpassword:
            errors['confirmpassword'] = "Confirm password is required."
        elif password != confirmpassword:
            errors['confirmpassword'] = "Passwords do not match."

        if not role:
            errors['role'] = "Role is required." 

        if errors:
            return render(request, 'signup.html', {'errors': errors})

       
        my_user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            email=email,
            username=username,
            password=password,
            role=role  
        )
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html', {'errors': {}})


#LOGIN LOGIC
def LoginPage(request):
    if request.user.is_authenticated:
        print(f"Authenticated user: {request.user.username}")
        print(f"User role: {request.user.role}")
        
        if request.user.role == "property_manager":
            return redirect('propertyownerdashboard')
        elif request.user.role == "admin":
            return redirect('admin')
        else:
            return redirect('home')  # Redirect normal users to home

    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username:
            errors["username"] = "Username is required."
        if not password:
            errors["password"] = "Password is required."

        if not errors:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
            else:
                # Check if username exists in the database
                if not User.objects.filter(username=username).exists():
                    errors["username"] = "Username does not exist."
                else:
                    errors["password"] = "Incorrect password."

        return render(request, "login.html", {"errors": errors, "username": username})

    return render(request, "login.html", {"errors": {}})


#LOGOUT LOGIC
def LogoutPage(request):
    logout(request)
    return redirect('login')

#ABOUTUS PAGE LOGIC
def AboutPage(request):
    about_us = AboutUs.objects.first()  # Fetch the first record
    return render(request, 'aboutus.html', {'about_us': about_us})


#CONTACTPAGE LOGIC
def ContactPage(request):
    errors = {}
    is_not_logged_in = not request.user.is_authenticated  # Check if the user is logged in
    if request.method == 'POST':
        if is_not_logged_in:
            return render(request, 'contactus.html', {
                "is_not_logged_in": True, 
                "errors": errors
            })  
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')

        # Basic validation
        if not name:
            errors["name"] = "Name is required."
        if not phone:
            errors["phone"] = "Phone number is required"
        elif not re.match(r'^\d{10}$', phone):
            errors["phone"] = "Number must contain exactly 10 digits."
        if not subject:
            errors["subject"] = "Subject is required."
        if not message:
            errors["message"] = "Message is required."
        if not email:
            errors['email'] = "Email is required."
        else:
            try:
                validate_email(email) 
            except ValidationError:
                errors["email"] = "Enter a valid email address."
        if errors:
            return render(request, 'contactus.html', {"errors": errors, "name": name, "phone": phone, "subject": subject, "message": message, "email": email, "is_not_logged_in": is_not_logged_in,})
        
        
        # Save inquiry to the database
        contactus = ContactUs(name=name, phone=phone, subject=subject, message=message,email=email)
        contactus.save()
        messages.success(request, "Inquirey Sent Successfully")
        return redirect('contactus')
    
    return render(request, 'contactus.html', {"errors": {}, "is_not_logged_in": is_not_logged_in})

#HOMEPAGE LOGIC
def PropertyPage(request):
    properties = PropertyDetail.objects.all()  # Fetch all properties initially
    
    # Get the search filters from the GET request
    city = request.GET.get('city')
    property_type = request.GET.get('property_type')
    price_per_night = request.GET.get('price_per_night')

    # Apply filters based on user inputs
    if city:
        properties = properties.filter(Q(city__icontains=city))  # Fixed field name
    if property_type:
        properties = properties.filter(Q(property_type__icontains=property_type))  # Fixed field name
    if price_per_night:
        try:
            price_per_night = float(price_per_night)  # Convert to float
            properties = properties.filter(price_per_night__lte=price_per_night)  # Fixed field name
        except ValueError:
            pass  # Ignore invalid values
    
    return render(request, 'property.html', {'property': properties})


def property_detail(request, id):
    property_obj = get_object_or_404(PropertyDetail, id=id)  # Fetch property or return 404
    amenities_list = property_obj.amenities.split(", ") if property_obj.amenities else []  # Convert amenities to a list

    return render(request, 'propertydetail.html', {
        'property': property_obj,
        'amenities': amenities_list  # Pass as a list to template
    })

#Forgot Password
def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print("Email: ", email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("User Exists")
            send_mail("Reset Your Password", f"Hello User: {user}!\nTo reset password, click on the given link \n http://127.0.0.1:8000/newpassword/{user}", EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, "Password reset link has been sent to your email.")
        else:
            return render(request, 'forgotpassword.html', {"errors": {"email": "Email does not exist"}})
    return render(request, 'forgotpassword.html')

#New Password
def NewPasswordPage(request, user):
    userid = User.objects.get(username=user)
    errors = {}
    if request.method== "POST":
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        # Password validation pattern
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        # Validate password
        if not password:
            errors['password'] = "Password is required."
        elif not re.match(password_pattern, password):
            errors['password'] = "Password must be at least 8 characters, contain one uppercase, one lowercase, one number, and one special character." 
        # Validate confirm password
        if not confirmpassword:
            errors['confirmpassword'] = "Confirm password is required."
        elif password != confirmpassword:
            errors['confirmpassword'] = "Passwords do not match."

        # If there are errors, re-render the form with errors
        if errors:
            return render(request, 'newpassword.html', {'errors': errors})      
        if password == confirmpassword:
            userid.set_password(password)
            userid.save()
            return redirect('message')
    return render(request, 'newpassword.html')

#Message 
def Message(request):
    return render(request, 'message.html')
    
def my_account(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')

        # Validate the data
        if not first_name or not last_name or not email or not username:
            messages.error(request, "All fields are required.")
            return redirect('profile')  # Redirect back to the same page

        # Update user model fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        try:
            # Save the updated user details to the database
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

        return redirect('my_account')  # After saving, redirect to the same page

    return render(request, 'profile.html', {'user': user})

def saved(request):
    return render(request, 'home.html')


def bookings(request):
    return render(request, 'home.html')

def PropertyAdd(request):
    if request.method == "POST":
        # Extract form data
        title = request.POST.get("propertyName", "")
        description = request.POST.get("propertyDescription", "")
        property_type = request.POST.get("propertyType", "")
        street_address = request.POST.get("streetAddress", "")
        city = request.POST.get("city", "")
        country = request.POST.get("country", "")
        neighbourhood = request.POST.get("neighbourhood", "")
        num_kitchens = int(request.POST.get("numKitchens", 0))
        num_bedrooms = int(request.POST.get("numBedrooms", 0))
        num_bathrooms = int(request.POST.get("numBathrooms", 0))
        price_per_night = float(request.POST.get("pricePerNight", 0))
        availability = request.POST.get("availability", "")
        license_number = request.POST.get("licenseNumber", "")
        amenities = request.POST.getlist("amenities")  # Multiple amenities as a list
        thumbnail = request.FILES.get("thumbnail")  # Single thumbnail image
        images = request.FILES.getlist("propertyImages")  # Multiple property images

        # Ensure required fields are not empty
        if not title or not description or not property_type or not city or not country:
            messages.error(request, "Please fill in all required fields.")
            return redirect('owner_add_property')  # Redirect to the same page to show the error message

        # Save the Property object
        property_obj = PropertyDetail(
            title=title,
            description=description,
            property_type=property_type,
            street_address=street_address,
            city=city,
            country=country,
            neighbourhood=neighbourhood,
            num_kitchens=num_kitchens,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            price_per_night=price_per_night,
            availability=availability,
            license_number=license_number,
            amenities=", ".join(amenities)  # Store as comma-separated values
        )
        property_obj.save()

        # Save the thumbnail image if exists
        if thumbnail:
            PropertyImage.objects.create(property=property_obj, image=thumbnail)

        # Save multiple property images if any exist
        for image in images:
            PropertyImage.objects.create(property=property_obj, image=image)

        approved_properties = PropertyDetail.objects.filter(approval_status="approved")
    
        messages.success(request, "Property Submitted Successfully!")
        return redirect("propertyadd")  # Redirect to the dashboard or another page

    return render(request, 'propertyadd.html')


def Propertyownerdashboard(request):
    return render(request, 'propertyownerdashboard.html')        
        
        
        