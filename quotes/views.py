from django.shortcuts import render
import random

# Hardcoded list of quotes and image URLs
QUOTES = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Innovation distinguishes between a leader and a follower. – Steve Jobs",
    "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
    "Don’t let the noise of others’ opinions drown out your own inner voice. – Steve Jobs",
    "You can’t connect the dots looking forward; you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future. – Steve Jobs"

]

IMAGES = [
      # Replace with actual image URLs or paths
    "images/SteveJobs1.jpg",
    "images/SteveJobs2.jpg",
"images/SteveJobs3.jpg",
"images/SteveJobs4.jpg",


 
]

# View for the main page and /quote
def quote(request):
    selected_quote = random.choice(QUOTES)
    selected_image = random.choice(IMAGES)
    context = {
        'quote': selected_quote,
        'image': selected_image
    }
    return render(request, 'quoteapp/quote.html', context)

# View to show all quotes and images
def show_all(request):
    context = {
        'quotes': QUOTES,
        'images': IMAGES
    }
    return render(request, 'quoteapp/show_all.html', context)

# View for the about page
def about(request):
    context = {
        'biography': "Steve Jobs was the founder of Apple and one of the most influential entrepreneur",
    }
    return render(request, 'quoteapp/about.html', context)
