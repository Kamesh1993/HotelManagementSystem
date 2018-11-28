from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (login,
                                 authenticate,
                                 get_user_model,
                                 logout,
                                 )
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegisterForm(forms.Form):
    firstname = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    lastname = forms.CharField(max_length=150)
    address = forms.CharField(max_length=450)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter Email')
    password = forms.CharField(label = 'Enter Password', widget=forms.PasswordInput)

class RoomBooking(forms.Form):
    checkin = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y"),required=True)
    checkout = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y"),required=False)
    room = forms.CharField()

class Reservation(forms.Form):
    firstname = forms.CharField()
    middlename = forms.CharField()
    lastname = forms.CharField()
    email = forms.EmailField()
    phone = forms.IntegerField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipcode = forms.IntegerField()
    idproof = forms.CharField()
    rooms = forms.IntegerField()