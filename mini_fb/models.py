"""
Afzal Khan
afzalk@bu.edu
Description: This file defines the Profile model and includes fields for first name, last name, city, email, and profile image URL.
"""
from django.db import models



class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
