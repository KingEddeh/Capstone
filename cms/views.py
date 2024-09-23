from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import csv
from .models import *
from .forms import *
from .filters import *

from django.db.models import Count, DateTimeField, Sum, F, Q
from django.db.models.functions import TruncHour, TruncDay, TruncMonth, TruncYear
from django.utils.timezone import localtime
from django.utils import timezone
from collections import defaultdict
from django.utils.timezone import localtime, is_naive, make_aware
from datetime import datetime, timedelta

from django.db.models.functions import Coalesce

from django.db import transaction, IntegrityError

import calendar

from django.contrib import messages
from django.db.models import RestrictedError


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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)  # Log out the current user
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url="Login")
def dashboard_view(request):

    # for dates
    today = timezone.localdate()
    one_month_later = today + timedelta(days=30)

    # PATIENT CARD---------------------------------------------------

    # statistic 1:
    number_of_patients = patient.objects.all().count()

    # statistic 2:
    treatment_count = Treatment_logbook.objects.filter(created_at__date=today).count()
    referral_count = Referral.objects.filter(created_at__date=today).count()
    medical_certificate_count = Medicalcertificate_logbook.objects.filter(created_at__date=today).count()
    total_records_today = treatment_count + referral_count + medical_certificate_count

    # EXPIRING MEDICINES CARD-------------------------------------------

    expiring_stocks = Stock.objects.filter(expiration_date__lte=one_month_later, current_stock__gt=0, disposed=False).order_by('expiration_date')
    
    # LOW STOCKS CARD-------------------------------------------

    low_stocks = Stock.objects.filter(current_stock__lt=20, current_stock__gt=0, disposed=False)
    
    context = {
        'number_of_patients': number_of_patients,
        'total_records_today': total_records_today,
        'expiring_stocks': expiring_stocks,
        'low_stocks': low_stocks,
    }
    
    return render(request, 'cms/MainMenu.html', context)


#Patient
@login_required(login_url="Login")
def patientdata_view(request):

    myFilter = PatientFilter(request.GET, queryset=patient.objects.all().order_by('-id'))
    patients = myFilter.qs

    context = {'patients':patients, 'myFilter':myFilter}

    return render(request, 'cms/patient-data.html', context)

@login_required(login_url="Login")
def patientform_add_view(request):

    form = PatientForm()
    form_treatment = TreatmentForm()

    if request.method == "POST":
        form = PatientForm(request.POST)
        form_treatment = TreatmentForm(request.POST)

        if form.is_valid() and form_treatment.is_valid():
            with transaction.atomic():
                # Save patient form
                patient_instance = form.save(commit=False)
                if not patient_instance.provider:
                    patient_instance.provider = request.user.username
                patient_instance.provider_updated = request.user.username
                patient_instance.save()

                autofill_uniquenumber_in_form = patient_instance

                # Save treatment form
                treatment_instance = form_treatment.save(commit=False)
                if not treatment_instance.provider:
                    treatment_instance.provider = request.user.username
                treatment_instance.provider_updated = request.user.username
                treatment_instance.unique_number = autofill_uniquenumber_in_form
                treatment_instance.save()

            return redirect('Patient Data')

    context = {'form': form, 'form_treatment': form_treatment}
    return render(request, 'cms/patient-form.html', context)

@login_required(login_url="Login")
def patientform_update_view(request, pk):

    patient_instance = get_object_or_404(patient, id=pk)
    form = PatientForm(instance=patient_instance)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient_instance)
        if form.is_valid():
            patient_instance = form.save(commit=False)
            patient_instance.provider_updated = request.user.username
            if not patient_instance.provider:
                patient_instance.provider = request.user.username
            patient_instance.save()
            form.save()
            return redirect('Patient Data')

    context = {'form':form}

    return render(request, 'cms/patient-form.html', context)

@login_required(login_url="Login")
def patientform_delete_view(request, pk):
    p = get_object_or_404(patient, id=pk)
    if request.method == "POST":
        try:
            p.delete()
            return redirect('Patient Data')
        except RestrictedError as e:
            messages.error(request, f"{p} cannot be deleted with existing records. Error: {str(e)}")
    
    context = {'p': p}
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

    myFilter = MedcertFilter(request.GET, queryset=Medicalcertificate_logbook.objects.all().order_by('-id'))
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/medcert-data.html', context)

@login_required(login_url="Login")
def medcertform_add_view(request):

    form = MedcertForm()
    if request.method == "POST":
        form = MedcertForm(request.POST)
        if form.is_valid():
            medcert_instance = form.save(commit=False)
            medcert_instance.provider_updated = request.user.username
            if not medcert_instance.provider:
                medcert_instance.provider = request.user.username
            medcert_instance.save()
            return redirect('Medcert Data')

    context = {'form':form}

    return render(request, 'cms/medcert-form.html', context)

@login_required(login_url="Login")
def medcertform_update_view(request, pk):

    referral_instance = get_object_or_404(Medicalcertificate_logbook, id=pk)
    form = MedcertForm(instance=referral_instance)
    if request.method == "POST":
        form = MedcertForm(request.POST, instance=referral_instance)
        if form.is_valid():
            medcert_instance = form.save(commit=False)
            medcert_instance.provider_updated = request.user.username
            if not medcert_instance.provider:
                medcert_instance.provider = request.user.username
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



#Referral
@login_required(login_url="Login")
def referraldata_view(request):

    myFilter = ReferralFilter(request.GET, queryset=Referral.objects.all().order_by('-id'))
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/referral-data.html', context)

@login_required(login_url="Login")
def referralform_add_view(request):

    form = ReferralForm()
    if request.method == "POST":
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral_instance = form.save(commit=False)
            referral_instance.provider_updated = request.user.username
            if not referral_instance.provider:
                referral_instance.provider = request.user.username
            referral_instance.save()
            return redirect('Referral Data')

    context = {'form':form}

    return render(request, 'cms/referral-form.html', context)

@login_required(login_url="Login")
def referralform_update_view(request, pk):

    referral_instance = get_object_or_404(Referral, id=pk)
    form = ReferralForm(instance=referral_instance)
    if request.method == "POST":
        form = ReferralForm(request.POST, instance=referral_instance)
        if form.is_valid():
            referral_instance = form.save(commit=False)
            referral_instance.provider_updated = request.user.username
            if not referral_instance.provider:
                referral_instance.provider = request.user.username
            form.save()
            return redirect('Referral Data')

    context = {'form':form}

    return render(request, 'cms/referral-form.html', context)

@login_required(login_url="Login")
def referralform_delete_view(request, pk):

    p = get_object_or_404(Referral, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Referral Data')

    context = {'p':p}

    return render(request, 'cms/referral-delete.html', context)

@login_required(login_url="Login")
def referralform_export_view(request):

    records = Referral.objects.all()
    myFilter = ReferralFilter(request.GET, queryset=records)
    records = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in Referral._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in records:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response



#Treatment Logbook
def treatmentdata_view(request, fk):

    if fk == '0':
        p = '0'
        myFilter = TreatmentFilter(request.GET, queryset=Treatment_logbook.objects.all().order_by('-id'))
    else:
        p = get_object_or_404(patient, id=fk)
        myFilter = TreatmentFilter(request.GET, queryset=Treatment_logbook.objects.filter(unique_number__id=fk))

    records = myFilter.qs

    if fk == '0':
        context = {'records':records, 'myFilter':myFilter, 'fk':fk}
    else:
        context = {'records':records, 'myFilter':myFilter, 'fk':fk, 'p':p}

    return render(request, 'cms/treatment-data.html', context)

@login_required(login_url="Login")
def treatmentform_add_view(request, fk):

    p = get_object_or_404(patient, id=fk)
    form_treatment = TreatmentForm()
    if request.method == "POST":
        form_treatment = TreatmentForm(request.POST)
        if form_treatment.is_valid():
            treatment_instance = form_treatment.save(commit=False)
            if not treatment_instance.provider:
                treatment_instance.provider = request.user.username
            treatment_instance.provider_updated = request.user.username
            treatment_instance.unique_number = p
            form_treatment.save()
            return redirect('Treatment Data', fk=fk)

    context = {'form_treatment':form_treatment, 'p':p}

    return render(request, 'cms/treatment-form.html', context)

@login_required(login_url="Login")
def treatmentform_update_view(request, pk):

    treatment_instance = get_object_or_404(Treatment_logbook, id=pk)
    form_treatment = TreatmentForm(instance=treatment_instance)
    if request.method == "POST":
        form_treatment = TreatmentForm(request.POST, instance=treatment_instance)
        if form_treatment.is_valid():
            treatment_instance = form_treatment.save(commit=False)
            if not treatment_instance.provider:
                treatment_instance.provider = request.user.username
            treatment_instance.provider_updated = request.user.username
            form_treatment.save()
            return redirect('Treatment Data', fk=0)

    context = {'form_treatment':form_treatment}

    return render(request, 'cms/treatment-form.html', context)

@login_required(login_url="Login")
def treatmentform_delete_view(request, pk):

    p = get_object_or_404(Treatment_logbook, id=pk)
    if request.method == "POST":
        try:
            p.delete()
            return redirect('Treatment Data', fk=p.unique_number.id)
        except RestrictedError as e:
            messages.error(request, f"{p} cannot be deleted with existing prescriptions referencing this treatment record. Error: {str(e)}")

    context = {'p':p}

    return render(request, 'cms/treatment-delete.html', context)

@login_required(login_url="Login")
def treatmentform_export_view(request):

    records = Treatment_logbook.objects.all()
    myFilter = TreatmentFilter(request.GET, queryset=records)
    records = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in Treatment_logbook._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in records:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response



#Inventory----------------------------------------------------------------

@login_required(login_url="Login")
def inventorydata_view(request):

    myFilter = InventoryFilter(request.GET, queryset=Stock.objects.all().order_by('-id'))
    records = myFilter.qs

    context = {'records': records, 'myFilter': myFilter}

    return render(request, 'cms/inventory-data.html', context)

@login_required(login_url="Login")
def inventoryform_add_view(request):

    form = InventoryForm()
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory_instance = form.save(commit=False)
            if not inventory_instance.provider:
                inventory_instance.provider = request.user.username
            inventory_instance.provider_updated = request.user.username
            form.save()
            return redirect('Inventory Data')

    context = {'form':form}

    return render(request, 'cms/inventory-form.html', context)

@login_required(login_url="Login")
def inventoryform_update_view(request, pk):

    inventory_instance = get_object_or_404(Stock, id=pk)
    form = InventoryForm(instance=inventory_instance)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=inventory_instance)
        if form.is_valid():
            try:
                inventory_instance = form.save(commit=False)
                if not inventory_instance.provider:
                    inventory_instance.provider = request.user.username
                inventory_instance.provider_updated = request.user.username
                form.save()
            except IntegrityError as e:
                messages.error(request, f"Updated stock is less than the stock already used in prescriptions. Error: {str(e)}")
                return redirect('Inventory Update', pk=pk)

            return redirect('Inventory Data')
        
    context = {'form':form}

    return render(request, 'cms/inventory-form.html', context)

@login_required(login_url="Login")
def inventoryform_delete_view(request, pk):

    p = get_object_or_404(Stock, id=pk)
    if request.method == "POST":
        try:
            p.delete()
            return redirect('Inventory Data')
        except RestrictedError as e:
            messages.error(request, f"{p} cannot be deleted with exisitng prescriptions referencing this stock. Error:{str(e)}")
            return redirect('Inventory Delete', pk=pk)

    context = {'p':p}

    return render(request, 'cms/inventory-delete.html', context)

@login_required(login_url="Login")
def inventoryform_export_view(request):

    records = Stock.objects.all()
    myFilter = InventoryFilter(request.GET, queryset=records)
    records = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in Stock._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in records:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response



#medicine
@login_required(login_url="Login")
def medicinedata_view(request):

    myFilter = MedicineFilter(request.GET, queryset=Medicine.objects.all().order_by('-id'))
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/medicine-data.html', context)

@login_required(login_url="Login")
def medicineform_add_view(request):

    form = MedicineForm()
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine_instance = form.save(commit=False)
            if not medicine_instance.provider:
                medicine_instance.provider = request.user.username
            medicine_instance.provider_updated = request.user.username
            form.save()
            return redirect('Medicine Data')

    context = {'form':form}

    return render(request, 'cms/medicine-form.html', context)

@login_required(login_url="Login")
def medicineform_update_view(request, pk):

    medicine_instance = get_object_or_404(Medicine, id=pk)
    form = MedicineForm(instance=medicine_instance)
    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine_instance)
        if form.is_valid():
            medicine_instance = form.save(commit=False)
            if not medicine_instance.provider:
                medicine_instance.provider = request.user.username
            medicine_instance.provider_updated = request.user.username
            form.save()
            return redirect('Medicine Data')
        
    context = {'form':form}

    return render(request, 'cms/medicine-form.html', context)

@login_required(login_url="Login")
def medicineform_delete_view(request, pk):

    p = get_object_or_404(Medicine, id=pk)
    if request.method == "POST":
        try:
            p.delete()
            return redirect('Treatment Data', fk=p.unique_number.id)
        except RestrictedError as e:
            messages.error(request, f"{p} cannot be deleted with existing stocks referencing this medicine. Error: {str(e)}")

    context = {'p':p}

    return render(request, 'cms/medicine-delete.html', context)

@login_required(login_url="Login")
def medicineform_export_view(request):

    records = Medicine.objects.all()
    myFilter = MedicineFilter(request.GET, queryset=records)
    records = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in Medicine._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in records:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response



#Prescription
@login_required(login_url="Login")
def prescriptiondata_view(request, fk):

    p = get_object_or_404(Treatment_logbook, id=fk)
    myFilter = PrescriptionFilter(request.GET, queryset=Prescription.objects.filter(treatment_logbook__id=fk).order_by('-id'))
    records = myFilter.qs


    context = {'records':records, 'myFilter':myFilter, 'p':p}

    return render(request, 'cms/prescription-data.html', context)

@login_required(login_url="Login")
def prescriptionform_add_view(request, fk):

    p = get_object_or_404(Treatment_logbook, id=fk)
    form = PrescriptionForm()
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            try:
                prescription_instance = form.save(commit=False)
                if not prescription_instance.provider:
                    prescription_instance.provider = request.user.username
                prescription_instance.provider_updated = request.user.username
                prescription_instance.treatment_logbook = p
                form.save()
            except ValueError as e:
                messages.error(request, f"Not Enough Stock. Error: {str(e)}")
                return redirect('Prescription Add', fk=fk)

            return redirect('Prescription Data', fk=fk)

    context = {'form':form, 'p':p}

    return render(request, 'cms/prescription-form.html', context)

@login_required(login_url="Login")
def prescriptionform_update_view(request, pk, fk):

    p = get_object_or_404(Treatment_logbook, id=fk)
    prescription_instance = get_object_or_404(Prescription, id=pk)
    form = PrescriptionForm(instance=prescription_instance)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription_instance)
        if form.is_valid():
            try:
                prescription_instance = form.save(commit=False)
                if not prescription_instance.provider:
                    prescription_instance.provider = request.user.username
                prescription_instance.provider_updated = request.user.username
                form.save()
            except ValueError as e:
                messages.error(request, f"Not Enough Stock. Error: {str(e)}")
                return redirect('Prescription Add', fk=fk)

            return redirect('Prescription Data', fk=fk)
        
    context = {'form':form, 'p':p}

    return render(request, 'cms/prescription-form.html', context)

@login_required(login_url="Login")
def prescriptionform_delete_view(request, pk, fk):

    p = get_object_or_404(Prescription, id=pk)
    if request.method == "POST":
        try:
            p.delete()
        except RestrictedError as e:
            messages.error(request, "This item cannot be deleted due to foreign key constraints.")
            return redirect('Prescription Delete')

        return redirect('Prescription Data', fk=fk)

    context = {'p':p, 'fk':fk}

    return render(request, 'cms/prescription-delete.html', context)

@login_required(login_url="Login")
def prescriptionform_export_view(request):

    records = Prescription.objects.all()
    myFilter = PrescriptionFilter(request.GET, queryset=records)
    records = myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_queryset.csv"'
    
    writer = csv.writer(response)

    field_names = [
        field.name for field in Prescription._meta.get_fields() 
        if not field.is_relation or field.many_to_one
        ]
    writer.writerow(field_names)

    for obj in records:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response

@login_required(login_url="Login")
def chart_view(request):
    # Get query parameters
    selected_years = request.GET.getlist('years')
    selected_medicines = request.GET.getlist('medicines')
   
    # Convert years to integers
    years = [int(year) for year in selected_years]
   
    # Prepare data for each selected medicine
    data = []
    for medicine_id in selected_medicines:
        medicine = Medicine.objects.get(id=medicine_id).brand_name
        medicine_data = {
            'name': medicine,
            'stock_levels': [],
            'usage': []
        }
       
        cumulative_stock = 0  # Initialize cumulative stock
        for year in years:
            for month in range(1, 13):
                # Aggregate stock for the selected medicine across all entries
                stock_added = Stock.objects.filter(
                    medicine_id=medicine_id,
                    created_at__year=year,
                    created_at__month=month
                ).aggregate(total_stock=Sum(F('initial_stocks')))['total_stock'] or 0

                # Aggregate usage for the selected medicine across all prescriptions
                usage = Prescription.objects.filter(
                    medicine=medicine,
                    created_at__year=year,
                    created_at__month=month
                ).aggregate(total_usage=Sum('quantity_prescribed'))['total_usage'] or 0
                
                # Update cumulative stock
                cumulative_stock += stock_added - usage
                
                medicine_data['stock_levels'].append({
                    'x': f"{year}-{month:02d}",
                    'y': cumulative_stock
                })
                medicine_data['usage'].append({
                    'x': f"{year}-{month:02d}",
                    'y': usage
                })
       
        data.append(medicine_data)
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(data, safe=False)
   
    # If not an AJAX request, render the template
    medicines = Stock.objects.values('medicine_id', 'medicine__brand_name').distinct()
    years = Stock.objects.dates('created_at', 'year').distinct()
   
    return render(request, 'cms/chart.html', {
        'medicines': medicines,
        'years': years
    })

@login_required(login_url="Login")
def department_cases_view(request):
    # Get query parameters
    selected_year = request.GET.get('year')
    selected_month = request.GET.get('month')

    if selected_year and selected_month:
        # Fetch data for the selected month and year
        cases = Treatment_logbook.objects.filter(
            created_at__year=selected_year,
            created_at__month=selected_month
        ).values('category', 'unique_number__department').annotate(
            count=models.Count('id')
        )

        # Prepare data for the chart
        departments = patient._meta.get_field('department').choices
        categories = dict(Treatment_logbook._meta.get_field('category').choices)
        
        data = {dept[0]: {cat: 0 for cat in categories.keys()} for dept in departments}
        
        for case in cases:
            dept = case['unique_number__department']
            category = case['category']
            count = case['count']
            data[dept][category] = count

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(data)

    # If not an AJAX request or no year/month selected, render the template
    years = Treatment_logbook.objects.dates('created_at', 'year').distinct()
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]

    return render(request, 'cms/department_cases_chart.html', {
        'years': years,
        'months': months
    })

#API==================================================================================================
#for Patient visits
@login_required(login_url="Login")
def get_logbook_data(request):
    # Combine all three logbooks, truncating to the specified group
    medical_certificates = Medicalcertificate_logbook.objects.annotate(
        timestamp=TruncHour('created_at')
    ).values('timestamp').annotate(count=Count('id')).order_by('timestamp')
   
    treatments = Treatment_logbook.objects.annotate(
        timestamp=TruncHour('created_at')
    ).values('timestamp').annotate(count=Count('id')).order_by('timestamp')
   
    referrals = Referral.objects.annotate(
        timestamp=TruncHour('created_at')
    ).values('timestamp').annotate(count=Count('id')).order_by('timestamp')
   
    # Combine all data
    combined_data = list(medical_certificates) + list(treatments) + list(referrals)
   
    # Create a defaultdict to store the grouped data, initialize counts to 0
    grouped_data = defaultdict(lambda: {'count': 0})

    # Sort combined data by timestamp
    combined_data.sort(key=lambda entry: entry['timestamp'])

    if combined_data:
        # Get the first and last timestamps in the data
        start_time = combined_data[0]['timestamp']
        end_time = combined_data[-1]['timestamp']

        # Ensure the start and end times are aware (UTC)
        if is_naive(start_time):
            start_time = make_aware(start_time)
        if is_naive(end_time):
            end_time = make_aware(end_time)

        # Create a time range from the start to end with hourly intervals
        current_time = start_time
        while current_time <= end_time:
            local_time = localtime(current_time)  # Convert to local time
            formatted_time = local_time.isoformat()
            # Ensure the time is included in the grouped_data, even if no records
            grouped_data[formatted_time]['count'] += 0  # Set count to 0 if no record exists
            current_time += timedelta(hours=1)

    # Add actual counts from combined data
    for entry in combined_data:
        utc_time = entry['timestamp']
       
        # Ensure the timestamp is aware (UTC) before converting
        if is_naive(utc_time):
            utc_time = make_aware(utc_time)
       
        local_time = localtime(utc_time)  # Convert UTC to local time
       
        formatted_time = local_time.isoformat()
       
        grouped_data[formatted_time]['count'] += entry['count']
   
    # Transform data for ApexCharts
    series_data = {
        'name': 'Records',
        'data': [{'x': time, 'y': count['count']} for time, count in sorted(grouped_data.items())]
    }

    return JsonResponse([series_data], safe=False)
