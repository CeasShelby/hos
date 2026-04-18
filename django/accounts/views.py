from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import RegisterForm
from .models import Profile 
from hostels.models import Booking, RoommateProposal
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .form import CombinedProfilePreferenceForm
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
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Check if matched
    is_matched = RoommateProposal.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)),
        status='accepted'
    ).exists()
    
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'is_matched': is_matched
    })

@login_required
def edit_profile(request):
    # Check if already matched - LOCK PROFILE
    is_matched = RoommateProposal.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)),
        status='accepted'
    ).exists()
    
    # We no longer redirect; we let them see the page but it will be read-only in the template
    
    # Requirement: No booking = No survey (only if not matched)
    if not is_matched:
        booked_hostel = Booking.objects.filter(
            student=request.user,
            status__in=['Pending', 'Paid'],
        ).exists()
        
        if not booked_hostel:
            messages.info(request, "You need to book a hostel before you can fill in the roommate survey.")
            return redirect('hostel-index')

    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if is_matched:
            messages.error(request, "Your profile is locked because you have already been matched.")
            return redirect('edit-profile')
            
        form = CombinedProfilePreferenceForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile and roommate preferences were updated.")
            return redirect('recommendations') 
        else:
            # If the form is NOT valid, this will help us see the errors in the terminal
            print(form.errors) 
    else:
        form = CombinedProfilePreferenceForm(instance=profile)
        
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'is_matched': is_matched
    })

def logout_view(request):
    logout(request)
    return redirect('hostel-index')

@login_required
def update_preferences(request):
    # Preferences are now part of the unified profile page.
    booked_hostel = Booking.objects.filter(
        student=request.user,
        status__in=['Pending', 'Paid'],
    ).exists()
    if not booked_hostel:
        messages.info(request, "You need to book a hostel before filling roommate preferences.")
        return redirect('recommendations')
    return redirect('edit-profile')
