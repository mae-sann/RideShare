from django.shortcuts import render

def landing_page(request):
    """
    Renders the landing page for Campus RideShare.
    """
    return render(request, 'landing_page/landing.html')
