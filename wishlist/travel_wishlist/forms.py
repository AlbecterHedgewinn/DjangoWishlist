from Django import forms
from .models import Place

# Create a form for the Place model
# this will allow us to create and update Place instances
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'visited']