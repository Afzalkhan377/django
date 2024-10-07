"""
Afzal Khan
afzalk@bu.edu
Description: It includes the ShowAllProfilesView which displays all profile records from the database.
"""


from django.views.generic import ListView
from .models import Profile


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'