from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)


class CreateAuctionForm(forms.Form):
    title = forms.CharField(max_length=30)
    category = forms.CharField(max_length=30)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()