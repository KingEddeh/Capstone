from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django.utils import timezone
from datetime import timedelta
from .models import Medicalcertificate_logbook

class MedicalCertificateView(DetailView):
    model = Medicalcertificate_logbook
    template_name = 'cms/medical_certificate.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medcert = self.get_object()
        context['medcert'] = medcert
        context['valid_until'] = timezone.now() + timedelta(days=30)
        return context

class PDFMedicalCertificateView(WeasyTemplateResponseMixin, MedicalCertificateView):
    pdf_attachment = True
   
    def get_pdf_filename(self):
        obj = self.get_object()
        return f'medical-certificate-{obj.unique_number}-{timezone.now():%Y%m%d}.pdf'

    def get_pdf_options(self):
        return {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }