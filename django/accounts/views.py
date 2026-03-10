from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import RegisterForm
from .models import Profile 
from django.contrib.auth.decorators import login_required
from .form import ProfileUpdateForm # We will create this next
# Create your views here.



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone') # Grab phone from form

            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken') 
                return render(request, 'accounts/register.html', {'form': form})
            else:
                # STEP 1: Create the User (without phone)
                user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # STEP 2: Save phone to the Profile
                # We use get_or_create in case a signal already made a profile
                profile, created = Profile.objects.get_or_create(user=user)
                profile.phone = phone
                profile.save()
                
                login(request, user)
                return redirect('hostel-index')
    else: 
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request): 
    error_message = None
    if request.method == 'POST':
        un = request.POST.get('username')
        ps = request.POST.get('password')
        
        user = authenticate(username=un, password=ps)
        
        if user is not None:
            login(request, user)
            return redirect('hostel-index')
        else:
            error_message = 'Invalid credentials'
            
    return render(request, 'accounts/login.html', {'error': error_message})




@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # CHANGE THIS: Redirect straight to the matching page
            return redirect('recommendations') 
        else:
            # If the form is NOT valid, this will help us see the errors in the terminal
            print(form.errors) 
    else:
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'accounts/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('hostel-index')
