from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View,ListView, DetailView, CreateView, DeleteView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LiftProfile, LiftRecord, LiftPost, Friend, Comment, FriendRequest
from .forms import CreateProfileForm, LiftRecordForm, LiftPostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max 

class ShowAllProfilesView(LoginRequiredMixin, ListView):
    model = LiftProfile
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles'
    login_url = reverse_lazy('project:project_login')  # Use the custom login URL name

    # Override get_queryset to add search functionality
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Get the search query from the request

        if query:
            # Filter profiles based on first name (case-insensitive)
            queryset = queryset.filter(first_name__icontains=query)

        return queryset

    # Pass the search query back to the template for displaying in the search bar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Add the search query to the context
        return context
# View to show a single profile page
from django.db.models import Q

class ShowProfilePageView(DetailView):
    model = LiftProfile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_profile = self.object  # The profile being viewed
        user = self.request.user

        # Check if the logged-in user has a profile
        if user.is_authenticated and hasattr(user, 'liftprofile'):
            user_profile = user.liftprofile  # The logged-in user's profile

            # Profile picture or default
            context['profile_picture'] = target_profile.get_profile_picture()

            # Check if the logged-in user and target profile are friends
            context['is_friend'] = Friend.objects.filter(
                Q(profile1=user_profile, profile2=target_profile) |
                Q(profile1=target_profile, profile2=user_profile)
            ).exists()

            # Friend request relationships
            context['received_request'] = FriendRequest.objects.filter(sender=target_profile, receiver=user_profile).exists()
            context['friend_request'] = FriendRequest.objects.filter(sender=target_profile, receiver=user_profile).first()
            context['sent_request'] = FriendRequest.objects.filter(sender=user_profile, receiver=target_profile).exists()

        else:
            # For unauthenticated users or users without a profile
            context['profile_picture'] = target_profile.get_profile_picture()
            context['is_friend'] = False
            context['received_request'] = False
            context['sent_request'] = False

        return context
# View to create a profile
class CreateProfileView(CreateView):
    model = LiftProfile
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()  # Include user creation form
        return context

    def form_valid(self, form):
        user_creation_form = UserCreationForm(self.request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()  # Save the new user
            form.instance.user = user  # Link the user to the profile

            # Handle profile_picture upload
            if 'profile_picture' in self.request.FILES:
                form.instance.profile_picture = self.request.FILES['profile_picture']
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form) 

    def get_success_url(self):
        return reverse_lazy('project:project_profile', args=[self.object.pk])


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = LiftProfile
    form_class = CreateProfileForm
    template_name = 'project/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(LiftProfile, user=self.request.user)

    def form_valid(self, form):
        # Save the profile changes, including the profile picture
        if 'profile_picture' in self.request.FILES:
            form.instance.profile_picture = self.request.FILES['profile_picture']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project:project_profile', kwargs={'pk': self.object.pk})


# View to create a lift record
class CreateLiftRecordView(LoginRequiredMixin, CreateView):
    model = LiftRecord
    form_class = LiftRecordForm
    template_name = 'project/create_lift_record_form.html'

    def form_valid(self, form):
        form.instance.user = get_object_or_404(LiftProfile, user=self.request.user)  # Link to user profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project:project_profile', args=[self.request.user.liftprofile.pk])


# View to create a lift post
class CreateLiftPostView(LoginRequiredMixin, CreateView):
    model = LiftPost
    form_class = LiftPostForm
    template_name = 'project/create_lift_post_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()  
        kwargs['user'] = self.request.user  # Add the logged-in user to the kwargs
        return kwargs

    def form_valid(self, form):
        form.instance.user = get_object_or_404(LiftProfile, user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project:project_home')
# View to show a specific post's details
class ShowPostDetailView(DetailView):
    model = LiftPost
    template_name = 'project/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Add the comment form to the context
        return context


# Add Friend View
class AddFriendView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        current_user_profile = get_object_or_404(LiftProfile, user=request.user)
        other_profile = get_object_or_404(LiftProfile, pk=pk)
        current_user_profile.add_friend(other_profile)
        return redirect('project:project_profile', pk=pk)


# Friend Suggestions View
class FriendSuggestionsView(LoginRequiredMixin, TemplateView):
    template_name = 'project/friend_suggestions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.liftprofile
        sent_request_ids = user_profile.sent_requests.values_list('receiver_id', flat=True)
        suggestions = user_profile.get_friend_suggestions().exclude(id__in=sent_request_ids)
        context['friend_suggestions'] = suggestions
        context['sent_request_ids'] = list(sent_request_ids)
        return context
# Delete Lift Record View
class DeleteLiftRecordView(LoginRequiredMixin, DeleteView):
    model = LiftRecord
    template_name = 'project/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('project:project_profile', args=[self.object.user.pk])

    def dispatch(self, request, *args, **kwargs):
        record = self.get_object()
        if record.user != request.user.liftprofile:  # Restrict deletion to record owner
            return redirect('project:project_home')
        return super().dispatch(request, *args, **kwargs)


# Delete Lift Post View
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = LiftPost
    template_name = 'project/confirm_delete_post.html'

    def get_success_url(self):
        return reverse_lazy('project:project_profile', args=[self.object.user.pk])

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user.liftprofile:  # Restrict deletion to post owner
            return redirect('project:project_home')
        return super().dispatch(request, *args, **kwargs)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(LiftPost, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lift_post = post
            comment.user = request.user.liftprofile 
            comment.save()
        return redirect('project:project_post_detail', pk=pk)

class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
      
        if request.user.liftprofile == comment.lift_post.user or request.user.liftprofile == comment.user:
            comment.delete()
            return redirect('project:project_post_detail', pk=comment.lift_post.pk)
        else:
            return HttpResponseForbidden("You don't have permission to delete this comment.")


# Send Friend Request
class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        sender = request.user.liftprofile
        receiver = get_object_or_404(LiftProfile, pk=pk)
        if sender != receiver and not FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.create(sender=sender, receiver=receiver)
        return redirect('project:project_profile', pk=pk)

# Accept Friend Request
class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        friend_request = get_object_or_404(FriendRequest, pk=pk, receiver=request.user.liftprofile)
        Friend.objects.create(profile1=friend_request.sender, profile2=friend_request.receiver)
        friend_request.delete()
        return redirect('project:project_profile', pk=request.user.liftprofile.pk)

# Decline Friend Request
class DeclineFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        friend_request = get_object_or_404(FriendRequest, pk=pk, receiver=request.user.liftprofile)
        friend_request.delete()
        return redirect('project:project_profile', pk=request.user.liftprofile.pk)

class FriendRequestsView(LoginRequiredMixin, ListView):
    template_name = 'project/friend_requests.html'
    context_object_name = 'friend_requests'

    def get_queryset(self):
       
        return FriendRequest.objects.filter(receiver=self.request.user.liftprofile)

class UnfriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_profile = request.user.liftprofile
        friend_profile = get_object_or_404(LiftProfile, pk=pk)

        # Find and delete the friendship record
        friendship = Friend.objects.filter(
            (Q(profile1=user_profile) & Q(profile2=friend_profile)) |
            (Q(profile1=friend_profile) & Q(profile2=user_profile))
        )
        friendship.delete()

        return redirect('project:project_profile', pk=friend_profile.pk)

class LeaderboardView(LoginRequiredMixin, TemplateView):
    template_name = "project/leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.liftprofile
        friends = user_profile.get_friends()

        leaderboard_data = []

        # Function to calculate lift stats for a profile
        def get_lift_data(profile):
            lift_records = LiftRecord.objects.filter(user=profile)
            max_bench = lift_records.filter(lift_type="bench_press").aggregate(max_weight=Max("weight"))["max_weight"]
            max_squat = lift_records.filter(lift_type="squat").aggregate(max_weight=Max("weight"))["max_weight"]
            max_deadlift = lift_records.filter(lift_type="deadlift").aggregate(max_weight=Max("weight"))["max_weight"]

            total = sum(filter(None, [max_bench, max_squat, max_deadlift]))
            return {
                "friend": profile,
                "max_bench": max_bench if max_bench else "N/A",
                "max_squat": max_squat if max_squat else "N/A",
                "max_deadlift": max_deadlift if max_deadlift else "N/A",
                "total": total if total > 0 else "N/A",
            }

        # Add the logged-in user's data
        leaderboard_data.append(get_lift_data(user_profile))

        # Add each friend's data
        for friend in friends:
            leaderboard_data.append(get_lift_data(friend))

        # Sort leaderboard by total weight (descending) or name if totals are N/A
        leaderboard_data.sort(key=lambda x: (x["total"] if x["total"] != "N/A" else 0), reverse=True)

        context["leaderboard"] = leaderboard_data
        return context
