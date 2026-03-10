from django.shortcuts import render
from config.models import CountrySettings
from home.models import LandingPage
from blog.models import BlogPage

def landing_view(request):
    country = getattr(request, 'country', None)
    page = None

    # 1. Try to find enabled LandingPage for current country
    if country:
        page = LandingPage.objects.filter(country=country, enabled=True).first()
    
    # 2. Fallback: Try enabled LandingPage for default country (Bolivia)
    if not page:
        bo_country = CountrySettings.objects.filter(country_code='bo').first()
        if bo_country:
             page = LandingPage.objects.filter(country=bo_country, enabled=True).first()

    # 3. Final Fallback: First enabled page
    if not page:
         page = LandingPage.objects.filter(enabled=True).first()

    # 4. Ultimate Fallback: Just the first page available (even if disabled)
    if not page:
        page = LandingPage.objects.first()
    
    # Get recent blog posts (published) to display on homepage
    posts = BlogPage.objects.live().order_by('-date_published')[:3]

    context = {
        'page': page,
        'self': page, # Maintain compatibility 
        'posts': posts,
    }
    return render(request, 'home/landing.html', context)
