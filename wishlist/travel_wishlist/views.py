from django.shortcuts import render
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

# Create a view to show the list of places
# filter only unvisited places and order them by name
def place_list(request):
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places})