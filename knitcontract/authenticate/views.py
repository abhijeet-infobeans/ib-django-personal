from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomRegistrationForm, LoginForm
from django.contrib.auth.models import Group

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                guest_group = Group.objects.get(name='Guest')
                user.groups.add(guest_group)
                return redirect('login')
            except Exception as e:
                pass
    else:
        form = CustomRegistrationForm()
    return render(request,'authenticate/register.html',{'form': form}) 

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            pass
    return render(request,'authenticate/login.html',{'form':form})


def user_logout(request):
    logout(request)
    return redirect('login')