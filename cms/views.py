from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

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

    patients = patient.objects.all().order_by('-created_at')

    context = {'patients':patients}

    return render(request, 'cms/patient-data.html', context)

@login_required(login_url="Login")
def patientform_add_view(request):

    form = PatientForm()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Patient Data')

    context = {'form':form}

    return render(request, 'cms/patient-form.html', context)

@login_required(login_url="Login")
def patientform_update_view(request, pk):

    patient_instance = get_object_or_404(patient, id=pk)
    print(patient_instance)
    form = PatientForm(instance=patient_instance)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient_instance)
        if form.is_valid():
            form.save()
            return redirect('Patient Data')

    context = {'form':form}

    return render(request, 'cms/patient-form.html', context)

@login_required(login_url="Login")
def patientform_delete_view(request, pk):

    p = get_object_or_404(patient, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Patient Data')

    context = {'p':p}

    return render(request, 'cms/patient-delete.html', context)

@login_required(login_url="Login")
def inventory_view(request):
    return render(request, 'cms/inventory.html')