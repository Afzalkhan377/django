"""
Afzal Khan
afzalk@bu.edu
Description: This file contains Django class-based views for managing profile pages and status messages .
It includes views to display all profiles, individual profile pages, and forms for creating profiles and posting status messages.
"""

from django.views.generic import ListView, DetailView
from .models import Profile,StatusMessage
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.views.generic.edit import CreateView

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
     # View to display a single profile using Django's DetailView.
    # It fetches a Profile object and renders it in the 'show_profile.html' template.
    model = Profile
    template_name = 'mini_fb/show_profile.html'  
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    # View to handle the creation of a new profile using a form.
    # It renders a form and saves the profile upon submission.
    model = Profile
    form_class = CreateProfileForm 
    template_name = 'mini_fb/create_profile_form.html' 

    
    def get_success_url(self):
         # It redirects to the 'show_profile' page for the newly created profile.
        return reverse('show_profile', args=[self.object.pk])

class CreateStatusMessageView(CreateView):
     # View to handle the creation of a new status message linked to a specific profile.
    # It renders a form and saves the status message upon submission.
    
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

   
    def form_valid(self, form):
        # Override the form_valid method to set the profile for the status message before saving it.
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile  
        return super().form_valid(form)

    def get_success_url(self):
         # It redirects to the 'show_profile' page for the profile that the status message was added to.
        return reverse('show_profile', args=[self.kwargs['pk']])