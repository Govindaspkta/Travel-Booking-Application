from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, TravelOption

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class BookingForm(forms.ModelForm):
    number_of_seats=forms.IntegerField(
        min_value=1,
        label="Number of Seats",
        widget=forms.NumberInput(attrs=
        {'class': 'form-control',
         'min': '1',
         'value':'1',
         'required':'required'
         }))
    class Meta:
        model = Booking
        fields = ('number_of_seats',)

    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)

    def clean_number_of_seats(self):
        seats = self.cleaned_data['number_of_seats']
        if seats > self.travel_option.available_seats:
            raise forms.ValidationError("Not enough seats available.")
        return seats

class TravelOptionFilterForm(forms.Form):
    type = forms.ChoiceField(choices=[('', 'All')] + list(TravelOption.TRAVEL_TYPES), required=False) 
    source = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))