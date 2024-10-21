"""
Afzal Khan
afzalk@bu.edu
Description:This file defines the Profile and StatusMessage models for the mini_fb app. 
The Profile model includes fields for first name, last name, city, email, and a profile image URL.
The StatusMessage model links status messages to profiles and records timestamps and messages.
"""
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
     # Fields for the Profile model, defining first name, last name, city, email, and profile image URL.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        # String representation of the Profile, returning the full name.
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
         # Method to retrieve all status messages for this profile, ordered by the most recent first.
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.pk)])

class StatusMessage(models.Model):
      # Fields for the StatusMessage model, which links messages to profiles and includes timestamps and text.
    timestamp = models.DateTimeField(default=timezone.now)  
    message = models.TextField()  
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE) 

   
    def __str__(self):
        return f"{self.profile.first_name}'s status at {self.timestamp}: {self.message}"
    def get_images(self):
        return Image.objects.filter(status_message=self)
    


class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} for {self.status_message.message}"