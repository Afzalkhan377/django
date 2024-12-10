
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import FriendSuggestionsView,AddCommentView,DeleteCommentView,SendFriendRequestView, AcceptFriendRequestView, DeclineFriendRequestView, FriendRequestsView, UnfriendView,LeaderboardView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'project' 

urlpatterns = [

    path('', views.ShowAllProfilesView.as_view(), name='project_home'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='project_profile'),
    path('create-profile/', views.CreateProfileView.as_view(), name='project_create_profile'),
    path('create-lift-record/', views.CreateLiftRecordView.as_view(), name='project_create_lift_record'),
    path('create-lift-post/', views.CreateLiftPostView.as_view(), name='project_create_lift_post'),
    path('post/<int:pk>/', views.ShowPostDetailView.as_view(), name='project_post_detail'),
    path('add-friend/<int:pk>/', views.AddFriendView.as_view(), name='project_add_friend'),
    path('friend-suggestions/', views.FriendSuggestionsView.as_view(), name='project_friend_suggestions'),
    path('delete-lift-record/<int:pk>/', views.DeleteLiftRecordView.as_view(), name='project_delete_lift_record'),
    path('delete-post/<int:pk>/', views.DeletePostView.as_view(), name='project_delete_post'),
    path('friend-suggestions/', FriendSuggestionsView.as_view(), name='project_friend_suggestions'),
    path('profile/update/<int:pk>/', views.UpdateProfileView.as_view(), name='project_update_profile'),

    path('post/<int:pk>/add-comment/', AddCommentView.as_view(), name='project_add_comment'),
    path('comment/delete/<int:pk>/', DeleteCommentView.as_view(), name='project_delete_comment'),
    path('friend-requests/', FriendRequestsView.as_view(), name='project_friend_requests'),

    path('send-friend-request/<int:pk>/', SendFriendRequestView.as_view(), name='project_send_friend_request'),
    path('accept-friend-request/<int:pk>/', AcceptFriendRequestView.as_view(), name='project_accept_friend_request'),
    path('decline-friend-request/<int:pk>/', DeclineFriendRequestView.as_view(), name='project_decline_friend_request'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='project_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='project_logout'),
    path('unfriend/<int:pk>/', UnfriendView.as_view(), name='project_unfriend'),
    path('leaderboard/', LeaderboardView.as_view(), name='project_leaderboard'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])