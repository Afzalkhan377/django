from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote, name='quote'),         # Main page showing a random quote
    path('quote/', views.quote, name='quote'),   # Random quote, same as /
    path('show_all/', views.show_all, name='show_all'), # Page showing all quotes and images
    path('about/', views.about, name='about'),   # About page
]