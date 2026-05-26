from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm
from django.shortcuts import redirect, render


def _redirect_if_authenticated(request):
    if request.user.is_authenticated:
        return redirect('index')
    return None


def login(request):
    redirect_response = _redirect_if_authenticated(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'ex/login.html', {'form': form})


def register(request):
    redirect_response = _redirect_if_authenticated(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'ex/register.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('index')
