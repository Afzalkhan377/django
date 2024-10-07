"""
Afzal Khan
afzalk@bu.edu
Description: This file contains the URL patterns for the mini_fb application. It maps the root URL ('') to the ShowAllProfilesView.
"""

from django.urls import path
from .views import ShowAllProfilesView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
]
