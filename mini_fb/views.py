"""
Afzal Khan
afzalk@bu.edu
Description: This file contains Django class-based views for managing profile pages and status messages .
It includes views to display all profiles, individual profile pages, and forms for creating profiles and posting status messages.
"""
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,View
from .models import Profile,StatusMessage, Image
from django.urls import reverse,reverse_lazy
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm 
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


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



from django.urls import reverse_lazy


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        if 'user_creation_form' not in context:
            context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
      
        user_creation_form = UserCreationForm(self.request.POST)
        
        # Validate and save the user form
        if user_creation_form.is_valid():
            user = user_creation_form.save()  
            form.instance.user = user  # Attach the user to the profile instance
            
           
            return super().form_valid(form)
        else:
            
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirect to the profile page for the newly created profile
        return reverse_lazy('show_profile', args=[self.object.pk])

# View to create a new status message and handle image uploads
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_object(self):
        # Retrieve the Profile associated with the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    def form_valid(self, form):
        # Assign the profile of the logged-in user to the status message
        form.instance.profile = self.get_object()
        sm = form.save()

  
        files = self.request.FILES.getlist('files')
        for file in files:
            Image.objects.create(status_message=sm, image_file=file)

        
        return redirect('show_profile', pk=sm.profile.pk)

    def get_success_url(self):
        # Redirect to the profile page after successful creation
        return reverse('show_profile', args=[self.get_object().pk])


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        if 'user_creation_form' not in context:
            context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
      
        user_creation_form = UserCreationForm(self.request.POST)
        
        # Check if the user form is valid
        if user_creation_form.is_valid():
            # Save the new user and attach to the profile
            user = user_creation_form.save()
            form.instance.user = user  # Associate the user with the profile instance
            
            
            return super().form_valid(form)
        else:
            # If the user creation form is invalid, re-render the form with errors
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirect to the profile page of the newly created profile
        return reverse_lazy('show_profile', args=[self.object.pk])

# View to update profile information
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    def get_object(self):
        # Fetch the Profile associated with the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        # Redirect to the profile page after profile update
        return reverse('show_profile', args=[self.object.pk])

# View to delete a status message
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page after deleting the status message
        profile_pk = self.object.profile.pk
        return reverse('show_profile', args=[profile_pk])

# View to update the content of a status message
class UpdateStatusMessageView(LoginRequiredMixin,UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        # Redirect to the profile page after updating the status message
        profile_pk = self.object.profile.pk
        return reverse('show_profile', args=[profile_pk])
    
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        other_pk = self.kwargs['other_pk']
        
      
        profile = get_object_or_404(Profile, user=self.request.user)
        
       
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        # Add friend
        profile.add_friend(other_profile)
        
      
        return redirect(profile.get_absolute_url())

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self):
        # Fetch the Profile associated with the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_object(self):
        # Fetch the Profile associated with the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        context['news_feed'] = profile.get_news_feed() 
        return context