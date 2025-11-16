from django import forms
from .models import Place

# Create a form for the Place model
# this will allow us to create and update Place instances
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'visited']

# Create a date input model form field
class DateInput(forms.DateInput):
    input_type = 'date'

# Create a form for trip reviewing
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['notes', 'date_visited', 'photo']
        widgets = {
            'date_visited': DateInput(),
        }