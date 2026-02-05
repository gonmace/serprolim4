from django.shortcuts import render
from home.models import LandingPage
from blog.models import BlogPage

def landing_view(request):
    # Get the Landing Page
    page = LandingPage.objects.first()
    
    # Get recent blog posts (published) to display on homepage
    # 3posts seems to imply 3 posts
    posts = BlogPage.objects.live().order_by('-date_published')[:3]

    context = {
        'page': page,
        'self': page, # Maintain compatibility 
        'posts': posts,
    }
    return render(request, 'home/landing.html', context)
