from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Your Username', 
        min_length=5, 
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Email'
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']