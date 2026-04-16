from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from .form import HostelForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hostel, Booking
from django.db.models import Q # "Q" allows us to do complex "OR" searches
from accounts.models import Profile
import collections
from django.contrib.auth.models import User
from .models import RoommateProposal

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
    booking_form = BookingForm()
    return render(request, 'hostels/detail.html', {'hostel': hostel, 'booking_form': booking_form})



@login_required
def book_hostel(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)

    if request.method != 'POST':
        return redirect('hostel_detail', pk=pk)

    form = BookingForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please review your booking options and try again.")
        return redirect('hostel_detail', pk=pk)

    booking = form.save(commit=False)
    booking.student = request.user
    booking.hostel = hostel
    booking.status = 'Paid'  # TODO: replace with real payment confirmation

    if booking.room_type != 'double':
        booking.wants_roommate = False

    booking.save()

    if booking.room_type == 'double' and booking.wants_roommate:
        messages.success(request, "Booking successful! Now, please complete your roommate preference survey to find your match.")
        return redirect('edit-profile')

    messages.success(request, "Booking saved. You can view your bookings anytime.")
    return redirect('my-bookings')

@login_required
def my_bookings(request):
    # Systematic Lesson: We only want bookings where the student is the CURRENT user
    user_bookings = Booking.objects.filter(student=request.user).order_by('-booked_at')
    
    return render(request, 'hostels/my_bookings.html', {'bookings': user_bookings})


@login_required
def delete_booking(request, pk):
    # Fetch the booking or return 404 if it doesn't exist
    booking = get_object_or_404(Booking, id=pk, student=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Your booking has been cancelled successfully.")
        return redirect('my-bookings') # Or wherever you list their choices
        
    return render(request, 'hostels/confirm_delete.html', {'booking': booking})



@login_required
def hostel_recommendations(request):
    # 1. Verification Step: Does the user have valid data?
    my_profile = request.user.profile
    eligible_statuses = ['Pending', 'Paid']

    latest_booking = (
        Booking.objects.filter(
            student=request.user,
            status__in=eligible_statuses,
        )
        .select_related('hostel')
        .order_by('-booked_at')
        .first()
    )
    if not latest_booking:
        return render(request, 'hostels/recommendations.html', {
            'booking_needed': True,
        })

    # Prefer explicit roommate-enabled booking; fallback to latest booking for legacy records.
    explicit_match_booking = (
        Booking.objects.filter(
            student=request.user,
            status__in=eligible_statuses,
            room_type='double',
            wants_roommate=True,
        )
        .select_related('hostel')
        .order_by('-booked_at')
        .first()
    )
    my_booking = explicit_match_booking or latest_booking

    my_accepted = RoommateProposal.objects.filter(status='accepted').filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver').first()
    if my_accepted:
        partner = my_accepted.receiver if my_accepted.sender == request.user else my_accepted.sender
        return render(request, 'hostels/recommendations.html', {
            'already_paired': True,
            'paired_partner': partner,
            'hostel': my_booking.hostel,
        })

    # Check if the survey is incomplete (Cold Start check)
    is_incomplete = (
        my_profile.smoking_habit == 0
        or my_profile.study_time == 0
        or not my_profile.gender
        or not my_profile.age
    )
    
    if is_incomplete:
        # We send them to the same page, but with a 'survey_needed' flag
        return render(request, 'hostels/recommendations.html', {
            'survey_needed': True
        })
    if my_profile.smoking_habit == 0 or my_profile.study_time == 0:
        return render(request, 'hostels/no_survey.html') # Redirect to survey link

    # Exclude students already paired (accepted proposal either direction)
    accepted_pairs = RoommateProposal.objects.filter(status='accepted').values_list('sender_id', 'receiver_id')
    paired_user_ids = set()
    for a, b in accepted_pairs:
        paired_user_ids.add(a)
        paired_user_ids.add(b)

    # Only consider students in the SAME hostel and who completed the survey.
    # Backward compatibility: include roommate-enabled bookings OR legacy bookings from
    # students who already completed survey preferences.
    roommate_user_ids = (
        Booking.objects.filter(
            status__in=eligible_statuses,
            hostel=my_booking.hostel,
        )
        .filter(
            Q(room_type='double', wants_roommate=True) |
            Q(student__profile__smoking_habit__gt=0, student__profile__study_time__gt=0)
        )
        .exclude(student_id__in=paired_user_ids)
        .values_list('student_id', flat=True)
        .distinct()
    )

    # Only load participants of the SAME gender as the current user
    participants = list(
        Profile.objects.filter(user_id__in=roommate_user_ids)
        .exclude(smoking_habit=0)
        .exclude(study_time=0)
        .filter(gender=my_profile.gender)   # ← same-gender filter
    )
    
    def compatibility_details(source_profile, target_profile):
        smoke_sim = 5 - abs(source_profile.smoking_habit - target_profile.smoking_habit)
        study_sim = 5 - abs(source_profile.study_time - target_profile.study_time)

        smoke_weight = max(source_profile.smoking_weight, 1)
        study_weight = max(source_profile.study_weight, 1)
        base_score = (smoke_weight * smoke_sim) + (study_weight * study_sim)

        bonus = 0
        shared_traits = []
        if source_profile.cleanliness and source_profile.cleanliness == target_profile.cleanliness:
            bonus += 8
            shared_traits.append("Similar cleanliness")
        if source_profile.study_habit and source_profile.study_habit == target_profile.study_habit:
            bonus += 6
            shared_traits.append("Study style match")
        if source_profile.course and target_profile.course and source_profile.course.strip().lower() == target_profile.course.strip().lower():
            bonus += 4
            shared_traits.append("Same course")
        if source_profile.region and target_profile.region and source_profile.region.strip().lower() == target_profile.region.strip().lower():
            bonus += 3
            shared_traits.append("Same home region")
        if source_profile.religion and target_profile.religion and source_profile.religion.strip().lower() == target_profile.religion.strip().lower():
            bonus += 2
            shared_traits.append("Similar faith background")
        if source_profile.is_early_bird == target_profile.is_early_bird:
            bonus += 2
            shared_traits.append("Same day rhythm")

        total_score = base_score + bonus
        max_total_score = (smoke_weight * 5) + (study_weight * 5) + 25
        score_percent = int((total_score / max_total_score) * 100) if max_total_score else 0
        score_percent = max(0, min(100, score_percent))

        return total_score, score_percent, shared_traits[:3]

    # Compatibility Matrix: JSON-like structure (IDs only for Privacy)
    pref_lists = {}
    
    for s_a in participants:
        scores = []
        for s_b in participants:
            if s_a.id == s_b.id: continue
            
            score_a_to_b, _, _ = compatibility_details(s_a, s_b)
            scores.append({'id': s_b.id, 'score': score_a_to_b, 'username': s_b.user.username.lower()})
        
        # Preference Ranking: Sort descending by score
        scores.sort(key=lambda x: (-x['score'], x['username']))
        pref_lists[s_a.id] = [item['id'] for item in scores]

    # 3. Phase 2: Stable Matching (Gale-Shapley)
    free_students = list(pref_lists.keys())
    engagements = {} # {Receiver_ID: Proposer_ID}
    proposals_made = collections.defaultdict(int)

    while free_students:
        s_id = free_students.pop(0)
        s_prefs = pref_lists[s_id]
        
        if proposals_made[s_id] < len(s_prefs):
            r_id = s_prefs[proposals_made[s_id]]
            proposals_made[s_id] += 1
            
            if r_id not in engagements:
                engagements[r_id] = s_id
            else:
                s_prime_id = engagements[r_id]
                r_prefs = pref_lists[r_id]
                
                # If R prefers S over S' (Higher score = lower index in pref list)
                if r_prefs.index(s_id) < r_prefs.index(s_prime_id):
                    engagements[r_id] = s_id
                    free_students.append(s_prime_id)
                else:
                    free_students.append(s_id)

    # 4. Final Output & Identification
    my_match_id = None
    for r_id, s_id in engagements.items():
        if r_id == my_profile.id: my_match_id = s_id
        elif s_id == my_profile.id: my_match_id = r_id

    stable_match = Profile.objects.get(id=my_match_id) if my_match_id else None

    # --- New: List of potential matches with compatibility and proposal status ---
    matches = []

    for s_b in participants:
        if s_b.id == my_profile.id:
            continue
        score, percent, traits = compatibility_details(my_profile, s_b)

        # Proposal status
        proposal = RoommateProposal.objects.filter(sender=request.user, receiver=s_b.user).first()
        reverse_proposal = RoommateProposal.objects.filter(sender=s_b.user, receiver=request.user).first()
        status = None
        already_matched = False
        if proposal:
            status = proposal.status
            if status == 'accepted':
                already_matched = True
        elif reverse_proposal:
            status = reverse_proposal.status
            if status == 'accepted':
                already_matched = True

        matches.append({
            'user': s_b.user,
            'details': s_b,
            'score': percent,
            'proposal_status': status,
            'proposal': proposal,
            'reverse_proposal': reverse_proposal,
            'already_matched': already_matched,
            'traits': traits,
        })

    # Sort matches by compatibility score descending; tie-break by username for stable ordering
    matches.sort(key=lambda x: (-x['score'], x['user'].username.lower()))

    return render(request, 'hostels/recommendations.html', {
        'stable_match': stable_match,
        'profile': my_profile,
        'matches': matches,
        'hostel': my_booking.hostel,
    })



@login_required
def send_proposal(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if receiver == request.user:
        messages.info(request, "You cannot send a proposal to yourself.")
        return redirect('recommendations')

    my_booking = (
        Booking.objects.filter(
            student=request.user,
            status__in=['Pending', 'Paid'],
        )
        .filter(
            Q(room_type='double', wants_roommate=True) |
            Q(student__profile__smoking_habit__gt=0, student__profile__study_time__gt=0)
        )
        .order_by('-booked_at')
        .first()
    )
    receiver_booking = (
        Booking.objects.filter(
            student=receiver,
            status__in=['Pending', 'Paid'],
            hostel_id=my_booking.hostel_id if my_booking else None,
        )
        .filter(
            Q(room_type='double', wants_roommate=True) |
            Q(student__profile__smoking_habit__gt=0, student__profile__study_time__gt=0)
        )
        .order_by('-booked_at')
        .first()
    )
    if not my_booking or not receiver_booking:
        messages.info(request, "You can only propose to eligible students in your booked hostel.")
        return redirect('recommendations')

    if RoommateProposal.objects.filter(status='accepted').filter(Q(sender=request.user) | Q(receiver=request.user)).exists():
        messages.info(request, "You're already paired with a roommate.")
        return redirect('recommendations')
    if RoommateProposal.objects.filter(status='accepted').filter(Q(sender=receiver) | Q(receiver=receiver)).exists():
        messages.info(request, "That student is already paired with a roommate.")
        return redirect('recommendations')
    
    # Check if a proposal already exists
    exists = RoommateProposal.objects.filter(sender=request.user, receiver=receiver).exists()
    
    if not exists:
        RoommateProposal.objects.create(sender=request.user, receiver=receiver)
        messages.success(request, f"Proposal sent to {receiver.username}!")
    else:
        messages.info(request, "You have already sent a proposal to this student.")
        
    return redirect('recommendations')


@login_required
def proposals_inbox(request):
    # Get all proposals where the current user is the receiver
    incoming_proposals = RoommateProposal.objects.filter(
        receiver=request.user, 
        status='pending'
    ).order_by('-created_at')

    # Get all proposals where the current user is the sender (for feedback)
    sent_proposals = RoommateProposal.objects.filter(
        sender=request.user
    ).order_by('-created_at')
    
    return render(request, 'hostels/inbox.html', {
        'proposals': incoming_proposals,
        'sent_proposals': sent_proposals
    })

@login_required
def handle_proposal(request, proposal_id, action):
    proposal = get_object_or_404(RoommateProposal, id=proposal_id, receiver=request.user)
    
    if action == 'accept':
        proposal.status = 'accepted'
        # Once paired, remove both students from everyone else's lists by declining other pending proposals.
        RoommateProposal.objects.filter(
            status='pending'
        ).filter(
            Q(sender=proposal.sender) | Q(receiver=proposal.sender) | Q(sender=proposal.receiver) | Q(receiver=proposal.receiver)
        ).exclude(id=proposal.id).update(status='declined')
        messages.success(request, f"You are now roommates with {proposal.sender.username}!")
    else:
        proposal.status = 'declined'
        messages.info(request, "Proposal declined.")
        
    proposal.save()
    return redirect('proposals_inbox')