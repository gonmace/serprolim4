from .models import CountrySettings

class CountryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check for query parameter 'country'
        country_code = request.GET.get('country')
        
        if country_code:
            # Validate if it exists in DB
            if CountrySettings.objects.filter(country_code=country_code).exists():
                request.session['user_country'] = country_code
            else:
                # Optional: handle invalid code, e.g. revert to default or ignore
                pass

        # 2. Add 'country' attribute to request for easy access
        request.country = None
        user_country_code = request.session.get('user_country')
        
        if user_country_code:
            try:
                request.country = CountrySettings.objects.get(country_code=user_country_code)
            except CountrySettings.DoesNotExist:
                # Cleanup session if invalid
                del request.session['user_country']

        response = self.get_response(request)
        return response
