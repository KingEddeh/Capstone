import django_filters

from .models import *

class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = patient
        fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply additional filtering here if needed
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)

class MedcertFilter(django_filters.FilterSet):
    
    unique_number = django_filters.CharFilter()

    class Meta:
        model = Medicalcertificate_logbook
        fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply additional filtering here if needed
        return queryset

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset()
        request.session['filtered_queryset'] = list(filtered_queryset.values_list('id', flat=True))
        return super().get(request, *args, **kwargs)