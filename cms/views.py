from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Dashboard')
        else:
            return render(request, 'cms/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'cms/login.html', {'form': form})


@login_required(login_url="Login")
def dashboard_view(request):
    return render(request, 'cms/MainMenu.html')


@login_required(login_url="Login")
def patientdata_view(request):
    return render(request, 'cms/patient-data.html')

def inventory_view(request):
    return render(request, 'cms/inventory.html')