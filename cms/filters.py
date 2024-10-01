import django_filters
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput, DateInput, Select, NumberInput
from .models import *
from django_select2.forms import Select2Widget

class BootstrapFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.form.fields.values():
            if isinstance(field.widget, (TextInput, DateInput, Select)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, RangeWidget):
                field.widget.widgets[0].attrs.update({'class': 'form-control'})
                field.widget.widgets[1].attrs.update({'class': 'form-control'})

class PatientFilter(BootstrapFilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    contact_number = django_filters.NumberFilter(field_name='contact_number', widget=NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = patient
        fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class MedcertFilter(BootstrapFilterSet):
    unique_number__unique_number = django_filters.CharFilter(label="ID Number", widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__middle_name = django_filters.CharFilter(label="Middle Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__suffix = django_filters.CharFilter(label="Suffix", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Medicalcertificate_logbook
        fields = '__all__'
        exclude = ['unique_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class ReferralFilter(BootstrapFilterSet):
    unique_number__unique_number = django_filters.CharFilter(label="ID Number", widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__middle_name = django_filters.CharFilter(label="Middle Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__suffix = django_filters.CharFilter(label="Suffix", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    referred_hospital = django_filters.ChoiceFilter(
        choices=Referral.HOSPITAL_CHOICES,
        widget=Select2Widget(attrs={'class': 'form-control select2-widget'})
    )
    
    class Meta:
        model = Referral
        fields = '__all__'
        exclude = ['unique_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class TreatmentFilter(BootstrapFilterSet):
    unique_number__unique_number = django_filters.CharFilter(label="ID Number", widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__middle_name = django_filters.CharFilter(label="Middle Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    unique_number__suffix = django_filters.CharFilter(label="Suffix", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Treatment_logbook
        fields = '__all__'
        exclude = ['unique_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class MedicineFilter(BootstrapFilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Medicine
        fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class InventoryFilter(BootstrapFilterSet):
    medicine__brand_name = django_filters.CharFilter(label="Brand Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    medicine__generic_name = django_filters.CharFilter(label="Generic Name", lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control'}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Stock
        fields = '__all__'
        exclude = ['medicine', 'updated_at', 'stock_quantity', 'quantity_per_unit', 'expiration_date', 'initial_stocks', 'current_stock']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class PrescriptionFilter(BootstrapFilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    updated_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'form-control'})
    )
    quantity_prescribed = django_filters.NumberFilter(field_name='quantity_prescribed', widget=NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Prescription
        fields = '__all__'
        exclude = ['unique_number', 'updated_at', 'treatment_logbook']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)