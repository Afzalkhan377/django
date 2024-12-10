from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Friend(models.Model):
    profile1 = models.ForeignKey('LiftProfile', related_name='friend_profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey('LiftProfile', related_name='friend_profile2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} is friends with {self.profile2}"


class LiftProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    profile_picture = models.ImageField(upload_to='images/profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.city})"

    def get_profile_picture(self):
       
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default.jpeg' 
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.city})"
    def get_friends(self):
      
        friend_relationships = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        )
        friend_profiles = [
            rel.profile1 if rel.profile2 == self else rel.profile2
            for rel in friend_relationships
        ]
        return LiftProfile.objects.filter(id__in=[friend.id for friend in friend_profiles])

    @property
    def sent_requests(self):
        return FriendRequest.objects.filter(sender=self)

    @property
    def received_requests(self):
        return FriendRequest.objects.filter(receiver=self)
    def add_friend(self, other_profile):
        # Add a friend if not already friends
        if self == other_profile:
            return  # Cannot friend yourself
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other_profile) |
            models.Q(profile1=other_profile, profile2=self)
        ).exists()
        if not existing_friendship:
            Friend.objects.create(profile1=self, profile2=other_profile)

    def get_friend_suggestions(self):
        # Suggest profiles not already friends and not self
        friends = self.get_friends()
        suggestions = LiftProfile.objects.exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in friends])
        return suggestions

class LiftRecord(models.Model):
    LIFT_TYPES = [
        ('bench_press', 'Bench Press'),
        ('squat', 'Squat'),
        ('deadlift', 'Deadlift'),
    ]
    user = models.ForeignKey(LiftProfile, on_delete=models.CASCADE, related_name='lift_records')
    lift_type = models.CharField(max_length=20, choices=LIFT_TYPES)
    weight = models.FloatField()
    date_recorded = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.first_name} - {self.lift_type} ({self.weight} lbs)"


# Model for posts associated with a user's lift profile
class LiftPost(models.Model):
    user = models.ForeignKey(LiftProfile, on_delete=models.CASCADE, related_name='lift_posts')
    caption = models.TextField()
    lift_record = models.ForeignKey(LiftRecord, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) 

    def __str__(self):
        return f"Post by {self.user.first_name} on {self.created_at}"

# Model for comments on LiftPosts
class Comment(models.Model):
    lift_post = models.ForeignKey(LiftPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(LiftProfile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.first_name} on {self.lift_post}"

class FriendRequest(models.Model):
    sender = models.ForeignKey('LiftProfile', related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey('LiftProfile', related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Friend request from {self.sender} to {self.receiver}"