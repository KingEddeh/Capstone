import django_filters
from django_filters.widgets import RangeWidget
from .models import *


class PatientFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
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



class MedcertFilter(django_filters.FilterSet):
    unique_number__unique_number = django_filters.CharFilter(label="ID Number")
    unique_number__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains')
    unique_number__middle_name = django_filters.CharFilter(label="Middle Name", lookup_expr='icontains')
    unique_number__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains')
    unique_number__suffix = django_filters.CharFilter(label="Suffix", lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    class Meta:
        model = Medicalcertificate_logbook
        fields = '__all__'
        exclude = 'unique_number, updated_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)



class ReferralFilter(django_filters.FilterSet):
    unique_number__unique_number = django_filters.CharFilter(label="ID Number")
    unique_number__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains')
    unique_number__middle_name = django_filters.CharFilter(label="Middle Name", lookup_expr='icontains')
    unique_number__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains')
    unique_number__suffix = django_filters.CharFilter(label="Suffix", lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    class Meta:
        model = Referral
        fields = '__all__'
        exclude = 'unique_number, updated_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)



class TreatmentFilter(django_filters.FilterSet):
    unique_number__unique_number = django_filters.CharFilter(label="ID Number")
    unique_number__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains')
    unique_number__middle_name = django_filters.CharFilter(label="Middle Name", lookup_expr='icontains')
    unique_number__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains')
    unique_number__suffix = django_filters.CharFilter(label="Suffix", lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    class Meta:
        model = Treatment_logbook
        fields = '__all__'
        exclude = 'unique_number, updated_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)



class MedicineFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = 'updated_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)



class InventoryFilter(django_filters.FilterSet):
    medicine__brand_name = django_filters.CharFilter(label="Brand Name", lookup_expr='icontains')
    medicine__generic_name = django_filters.CharFilter(label="Generic Name", lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    class Meta:
        model = Stock
        fields = '__all__'
        exclude = 'medicine, updated_at, stock_quantity, quantity_per_unit, expiration_date'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)



class PrescriptionFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    class Meta:
        model = Prescription
        fields = '__all__'
        exclude = 'unique_number, updated_at, treatment_logbook'

    def get_queryset(self):
        #insert filters
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)