from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login

from .form import HostelForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hostel,Booking
from django.db.models import Q # "Q" allows us to do complex "OR" searches
from accounts.models import Profile

def hostel_list(request):
    # Start with all hostels
    hostels = Hostel.objects.all()

    # Feature: Search by Name
    query = request.GET.get('q')
    if query:
        hostels = hostels.filter(name__icontains=query)

    # Feature: Filter by Distance (Matching your outstanding features)
    dist = request.GET.get('distance')
    if dist:
        if dist == 'near':
            hostels = hostels.filter(distance_from_campus__lte=500)
        elif dist == 'boda':
            hostels = hostels.filter(distance_from_campus__gt=500)

    context = {
        'hostels': hostels,
    }
    return render(request, 'hostels/index.html', context)

def login_view(request):
    if request.method == 'POST':
        # ... (your existing authentication code) ...
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            # CHANGE THIS LINE from 'index' to your hostel list URL name
            return redirect('hostel-index') 
    # ...




@login_required
def add_hostel(request):
    if request.method == 'POST':
        # request.FILES is required for image uploads!
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.manager = request.user  # Link it to the logged-in manager
            hostel.save()
            return redirect('hostel-index')
    else:
        form = HostelForm()
    
    return render(request, 'hostels/add_hostel.html', {'form': form})

def hostel_detail(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    return render(request, 'hostels/detail.html', {'hostel': hostel})



@login_required
def book_hostel(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    
    # Create the booking automatically
    Booking.objects.create(
        student=request.user, 
        hostel=hostel
    )
    
    # Send a message to the student (optional but professional)
    return redirect('hostel_detail', pk=pk)

@login_required
def my_bookings(request):
    # Systematic Lesson: We only want bookings where the student is the CURRENT user
    user_bookings = Booking.objects.filter(student=request.user).order_by('-booked_at')
    
    return render(request, 'hostels/my_bookings.html', {'bookings': user_bookings})


@login_required
def delete_booking(request, booking_id):
    # Fetch the booking or return 404 if it doesn't exist
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Your booking has been cancelled successfully.")
        return redirect('my-bookings') # Or wherever you list their choices
        
    return render(request, 'hostels/confirm_delete.html', {'booking': booking})


@login_required
def hostel_recommendations(request):
    # 1. Get my profile or exit
    try:
        my_profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('edit-profile')

    # 2. Get the course filter and apply it ONCE
    course_query = request.GET.get('course')
    if course_query:
        all_profiles = Profile.objects.filter(course__icontains=course_query).exclude(user=request.user)
    else:
        all_profiles = Profile.objects.exclude(user=request.user)
    
    weights = {
        'study_habit': 40,
        'religion': 25,
        'cleanliness': 20,
        'is_early_bird': 10,
        'hobbies': 5
    }
    
    max_possible = sum(weights.values())
    roommate_matches = []

    # 3. Calculate scores
    for other in all_profiles:
        score = 0
        common_traits = []

        # Study Habit
        if my_profile.study_habit == other.study_habit:
            score += weights['study_habit']
            common_traits.append(f"{other.get_study_habit_display()} Study")

        # Religion
        if my_profile.religion and my_profile.religion.lower() == other.religion.lower():
            score += weights['religion']
            common_traits.append(other.religion)
            
        # Hobbies
        my_hobby_list = [h.strip().lower() for h in my_profile.hobbies.split(',')]
        other_hobby_list = [h.strip().lower() for h in other.hobbies.split(',')]
        shared = set(my_hobby_list).intersection(set(other_hobby_list))
        if shared:
            score += weights['hobbies']
            common_traits.append(f"Shares interest in {', '.join(shared)}")

        compatibility = int((score / max_possible) * 100)
        
        if compatibility >= 20: 
            roommate_matches.append({
                'user': other.user,
                'details': other,
                'score': compatibility,
                'traits': common_traits
            })

    roommate_matches.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'hostels/recommendations.html', {
        'matches': roommate_matches,
        'profile': my_profile
    })