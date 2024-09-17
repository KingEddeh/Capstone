from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import csv
from .models import *
from .forms import *
from .filters import *

from django.db.models import Count, DateTimeField
from django.db.models.functions import TruncHour, TruncDay, TruncMonth, TruncYear
from django.utils.timezone import localtime
from collections import defaultdict
from django.utils.timezone import localtime, is_naive, make_aware



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
    today = timezone.now().date()

    # PATIENT CARD---------------------------------------------------

    # statistic 1:
    number_of_patients = patient.objects.all().count()

    # statistic 2:
    treatment_count = Treatment_logbook.objects.filter(created_at__date=today).count()
    referral_count = Referral.objects.filter(created_at__date=today).count()
    medical_certificate_count = Medicalcertificate_logbook.objects.filter(created_at__date=today).count()
    total_records_today = treatment_count + referral_count + medical_certificate_count

    # Patient Visit Chart-------------------------------------------

    

    context = {
        'number_of_patients': number_of_patients,
        'total_records_today': total_records_today,
    }
    
    return render(request, 'cms/MainMenu.html', context)


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
            medcert_instance = form.save(commit=False)
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

    myFilter = ReferralFilter(request.GET, queryset=Referral.objects.all())
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
def treatmentdata_view(request):

    myFilter = TreatmentFilter(request.GET, queryset=Treatment_logbook.objects.all())
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/treatment-data.html', context)

@login_required(login_url="Login")
def treatmentform_add_view(request):

    form = TreatmentForm()
    if request.method == "POST":
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.provider = request.user.username
            form.save()
            return redirect('Treatment Data')

    context = {'form':form}

    return render(request, 'cms/treatment-form.html', context)

@login_required(login_url="Login")
def treatmentform_update_view(request, pk):

    treatment_instance = get_object_or_404(Treatment_logbook, id=pk)
    form = TreatmentForm(instance=treatment_instance)
    if request.method == "POST":
        form = TreatmentForm(request.POST, instance=treatment_instance)
        if form.is_valid():
            form.save()
            return redirect('Treatment Data')

    context = {'form':form}

    return render(request, 'cms/treatment-form.html', context)

@login_required(login_url="Login")
def treatmentform_delete_view(request, pk):

    p = get_object_or_404(Treatment_logbook, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Treatment Data')

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

    myFilter = InventoryFilter(request.GET, queryset=Stock.objects.all().order_by('expiration_date'))
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/inventory-data.html', context)

@login_required(login_url="Login")
def inventoryform_add_view(request):

    form = InventoryForm()
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.provider = request.user.username
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
            form.save()
            return redirect('Inventory Data')
        
    context = {'form':form}

    return render(request, 'cms/inventory-form.html', context)

@login_required(login_url="Login")
def inventoryform_delete_view(request, pk):

    p = get_object_or_404(Stock, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Inventory Data')

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

    myFilter = MedicineFilter(request.GET, queryset=Medicine.objects.all())
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/medicine-data.html', context)

@login_required(login_url="Login")
def medicineform_add_view(request):

    form = MedicineForm()
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.provider = request.user.username
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
            form.save()
            return redirect('Medicine Data')
        
    context = {'form':form}

    return render(request, 'cms/medicine-form.html', context)

@login_required(login_url="Login")
def medicineform_delete_view(request, pk):

    p = get_object_or_404(Medicine, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Medicine Data')

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

    myFilter = PrescriptionFilter(request.GET, queryset=Prescription.objects.filter(treatment_logbook__id=fk))
    records = myFilter.qs

    context = {'records':records, 'myFilter':myFilter}

    return render(request, 'cms/prescription-data.html', context)

@login_required(login_url="Login")
def prescriptionform_add_view(request):

    form = PrescriptionForm()
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.provider = request.user.username
            form.save()
            return redirect('Treatment Data')

    context = {'form':form}

    return render(request, 'cms/prescription-form.html', context)

@login_required(login_url="Login")
def prescriptionform_update_view(request, pk):

    prescription_instance = get_object_or_404(Prescription, id=pk)
    form = PrescriptionForm(instance=prescription_instance)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription_instance)
        if form.is_valid():
            form.save()
            return redirect('Treatment Data')
        
    context = {'form':form}

    return render(request, 'cms/prescription-form.html', context)

@login_required(login_url="Login")
def prescriptionform_delete_view(request, pk):

    p = get_object_or_404(Prescription, id=pk)
    if request.method == "POST":
        p.delete()
        return redirect('Treatment Data')

    context = {'p':p}

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

def chart_view(request):
    
    return render(request, 'cms/chart.html')


#API==================================================================================================
#for Patient visits
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
   
    # Aggregate data by the specified group
    grouped_data = defaultdict(lambda: {'count': 0})
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
        'data': [{'x': time, 'y': count['count']} for time, count in grouped_data.items()]
    }

    return JsonResponse([series_data], safe=False)


