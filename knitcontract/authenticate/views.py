from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegistrationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = CustomRegistrationForm()
    return render(request,'authenticate/register.html',{'form': form})   