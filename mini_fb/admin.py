"""
Afzal Khan
afzalk@bu.edu
Description: This file registers the Profile model and Status Message with the Django admin site so that it can be managed through the admin interface.
"""
from django.contrib import admin
from .models import Profile,Image
from .models import StatusMessage,Friend


admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)