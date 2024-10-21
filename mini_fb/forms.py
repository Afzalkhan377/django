"""
Afzal Khan
afzalk@bu.edu
Description: This file defines the forms for creating a new Profile and StatusMessage in the mini_fb app. 
The CreateProfileForm allows users to enter profile details, including first name, last name, city, birth date, and profile image URL.
The CreateStatusMessageForm allows users to create and submit a status message.
the updateprofileform allows user to update their email,image, location
"""

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    #Form for creating a new Profile. 
    #It allows users to input their first name, last name, city, birth date, and profile image URL.

    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 1920, -1)), label="Birth Date")
    email = forms.EmailField(label="Email", required=True)  # Added email field

    class Meta:
        model = Profile 
        fields = ['first_name', 'last_name', 'city', 'birth_date','email', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    # Form for creating a new StatusMessage. It allows users to input a message that will be linked to a profile.
    class Meta:
        model = StatusMessage
        fields = ['message'] 

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Exclude first_name and last_name from the fields that can be updated
        fields = ['profile_image_url', 'city', 'email']

