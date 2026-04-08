# hostels/context_processors.py
from .models import RoommateProposal

def proposal_count(request):
    if request.user.is_authenticated:
        # Count only 'pending' requests where the user is the receiver
        count = RoommateProposal.objects.filter(receiver=request.user, status='pending').count()
    else:
        count = 0
    return {'pending_proposals_count': count}