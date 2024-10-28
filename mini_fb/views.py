"""
Afzal Khan
afzalk@bu.edu
Description: This file contains Django class-based views for managing profile pages and status messages .
It includes views to display all profiles, individual profile pages, and forms for creating profiles and posting status messages.
"""
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,View
from .models import Profile,StatusMessage, Image
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm 
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

# View to create a new status message and handle image uploads
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        # Add profile data to the context
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # Save status message and handle associated image uploads
        sm = form.save(commit=False)
        sm.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        sm.save()

        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()

        return redirect('show_profile', pk=sm.profile.pk)

    def get_success_url(self):
        # Redirect to the profile page after successful creation
        return reverse('show_profile', args=[self.kwargs['pk']])

# View to update profile information
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        # Redirect to the profile page after profile update
        return reverse('show_profile', args=[self.object.pk])

# View to delete a status message
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page after deleting the status message
        profile_pk = self.object.profile.pk
        return reverse('show_profile', args=[profile_pk])

# View to update the content of a status message
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        # Redirect to the profile page after updating the status message
        profile_pk = self.object.profile.pk
        return reverse('show_profile', args=[profile_pk])

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']
        
        # Get the profile instances
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        # Add friend
        profile.add_friend(other_profile)
        
        # Redirect back to the profile page
        return redirect(profile.get_absolute_url())


class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['profile'] = profile
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context


class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['profile'] = profile
        context['news_feed'] = profile.get_news_feed()
        return context