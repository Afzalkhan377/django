"""
Afzal Khan
afzalk@bu.edu
Description: This file registers the Profile model with the Django admin site so that it can be managed through the admin interface.
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)