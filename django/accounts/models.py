

from typing import List, Dict, Tuple, Optional
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default='')
    age = models.PositiveIntegerField(null=True, blank=True)

    RELIGIOUS_CHOICES = [
        ('quietly', 'Quietly (Personal/Silent)'),
        ('loud', 'Loud (Speaking/Chanting)'),
        ('vocal', 'Vocal (Singing/Community)'),
    ]
    STUDY_SPOT_CHOICES = [
        ('hostel', 'Hostel'),
        ('library', 'Campus Library'),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    is_early_bird = models.BooleanField(default=True)
    
    # Priority Habits & Weights
    smoking_habit = models.IntegerField(default=0)
    smoking_weight = models.IntegerField(default=1)
    
    drinking_habit = models.IntegerField(default=0)
    drinking_weight = models.IntegerField(default=1)
    
    cleanliness_weight = models.IntegerField(default=1)
    
    religion_habit = models.CharField(max_length=20, choices=RELIGIOUS_CHOICES, default='quietly')
    religion_weight = models.IntegerField(default=1)
    
    noise_habit = models.IntegerField(default=0)
    noise_weight = models.IntegerField(default=1)

    # Other Habits
    study_time = models.IntegerField(default=0)
    study_weight = models.IntegerField(default=1)
    study_spot = models.CharField(max_length=10, choices=STUDY_SPOT_CHOICES, default='hostel')
    visitors_habit = models.IntegerField(default=0)
    
    religion = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True, help_text="Home Region/District")
    hobbies = models.TextField(blank=True, help_text="List a few things you love")
    
    CLEAN_CHOICES = [
        ('neat', 'Very Neat/Organized'),
        ('average', 'Average'),
        ('relaxed', 'Relaxed/Messy'),
    ]
    cleanliness = models.CharField(max_length=10, choices=CLEAN_CHOICES, default='average')
    course = models.CharField(max_length=100)
    study_habit = models.CharField(max_length=10, choices=[('quiet', 'Quiet'), ('group', 'Group')])

    def __str__(self):
        return f"{self.user.username}'s Profile"

# ---------------- Roommate Matching Engine ----------------
# Step 1: User Data Structure
class MatchUser:
    def __init__(self, user_id: int, habits: Dict[str, int], weights: Dict[str, int]):
        self.user_id = user_id
        self.habits = habits
        self.weights = weights

# Step 2: Compatibility Function (Weighted Sum Model)


    def recipient_prefers(new_id, current_id, recipient_id):
        recipient = next(u for u in users if u.user_id == recipient_id)
        new_score = calculate_compatibility(recipient, next(u for u in users if u.user_id == new_id))
        if current_id is None:
            return True
        current_score = calculate_compatibility(recipient, next(u for u in users if u.user_id == current_id))
        return new_score > current_score

    def match_roommates(users: List['MatchUser']) -> List[Tuple['MatchUser', Optional['MatchUser']]]:
        n = len(users)
        if n < 2:
            return [(users[0], None)] if n == 1 else []

        # Build preference lists for each user
        preferences = {}
        for user in users:
            others = [u for u in users if u.user_id != user.user_id]
            ranked = sorted(others, key=lambda u: -calculate_compatibility(user, u))
            preferences[user.user_id] = [u.user_id for u in ranked]

        # Gale-Shapley: everyone starts unmatched
        unmatched = set(user.user_id for user in users)
        proposals = {user.user_id: [] for user in users}
        matches = {}  # user_id -> partner_id

        while unmatched:
            proposer_id = unmatched.pop()
            proposer = next(u for u in users if u.user_id == proposer_id)
            # Propose to next highest not yet proposed
            for candidate_id in preferences[proposer_id]:
                if candidate_id not in proposals[proposer_id]:
                    proposals[proposer_id].append(candidate_id)
                    # If candidate is unmatched, match
                    if candidate_id not in matches:
                        matches[proposer_id] = candidate_id
                        matches[candidate_id] = proposer_id
                        break
                    else:
                        current_partner = matches[candidate_id]
                        if recipient_prefers(proposer_id, current_partner, candidate_id):
                            # Candidate prefers new proposer
                            matches[proposer_id] = candidate_id
                            matches[candidate_id] = proposer_id
                            # Old partner becomes unmatched
                            del matches[current_partner]
                            unmatched.add(current_partner)
                            break
            # If proposer couldn't find anyone, they remain unmatched

        # Build output pairs
        paired = set()
        result = []
        for user in users:
            if user.user_id in paired:
                continue
            partner_id = matches.get(user.user_id)
            if partner_id is not None and partner_id not in paired:
                partner = next(u for u in users if u.user_id == partner_id)
                result.append((user, partner))
                paired.add(user.user_id)
                paired.add(partner_id)
            elif user.user_id not in paired:
                result.append((user, None))
                paired.add(user.user_id)
        return result
    
 
 