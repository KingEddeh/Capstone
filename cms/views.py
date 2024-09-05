from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from .filters import *
import csv
from django.http import HttpResponse

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


#Patient
@login_required(login_url="Login")
def patientdata_view(request):

    myFilter = PatientFilter(request.GET, queryset=patient.objects.all())
    patients = myFilter.qs

    context = {'patients':patients, 'myFilter':myFilter}

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
def patientform_export_view(request):

    patients = patient.objects.all()
    myFilter = PatientFilter(request.GET, queryset=patients)
    patients = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in patient._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in patients:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response



#Logbook----------------------------------------

#Medcert
@login_required(login_url="Login")
def medcertdata_view(request):

    myFilter = MedcertFilter(request.GET, queryset=Medicalcertificate_logbook.objects.all())
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/medcert-data.html', context)

@login_required(login_url="Login")
def medcertform_add_view(request):

    form = MedcertForm()
    if request.method == "POST":
        form = MedcertForm(request.POST)
        if form.is_valid():
            #add provider name to field from logged in user
            instance = form.save(commit=False)
            instance.provider = request.user.username
            instance.save()
            return redirect('Medcert Data')

    context = {'form':form}

    return render(request, 'cms/medcert-form.html', context)

@login_required(login_url="Login")
def medcertform_update_view(request, pk):

    medcert_instance = get_object_or_404(Medicalcertificate_logbook, id=pk)
    form = MedcertForm(instance=medcert_instance)
    if request.method == "POST":
        form = MedcertForm(request.POST, instance=medcert_instance)
        if form.is_valid():
            form.save()
            return redirect('Medcert Data')

    context = {'form':form}

    return render(request, 'cms/medcert-form.html', context)

@login_required(login_url="Login")
def medcertform_delete_view(request, pk):

    p = get_object_or_404(Medicalcertificate_logbook, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Medcert Data')

    context = {'p':p}

    return render(request, 'cms/medcert-delete.html', context)

@login_required(login_url="Login")
def medcertform_export_view(request):

    records = Medicalcertificate_logbook.objects.all()
    myFilter = MedcertFilter(request.GET, queryset=records)
    records = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in Medicalcertificate_logbook._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in records:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response




#Inventory
@login_required(login_url="Login")
def inventory_view(request):
    return render(request, 'cms/inventory.html')