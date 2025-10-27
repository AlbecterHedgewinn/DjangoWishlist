from django.shortcuts import render
from .models import Place

# Create your views here.

# Create a view to show the list of places
def place_list(request):
    places = Place.objects.all()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places})