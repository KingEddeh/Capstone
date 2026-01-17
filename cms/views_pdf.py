from django.views.generic import DetailView
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound
from .models import Medicalcertificate_logbook

try:
    from xhtml2pdf import pisa  # type: ignore
    XHTML2PDF_AVAILABLE = True
except Exception:
    pisa = None
    XHTML2PDF_AVAILABLE = False


class MedicalCertificateView(DetailView):
    model = Medicalcertificate_logbook
    template_name = 'cms/medical_certificate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medcert = self.get_object()
        context['medcert'] = medcert
        context['valid_until'] = timezone.now() + timedelta(days=30)
        return context


class PDFMedicalCertificateView(MedicalCertificateView):
    """View that returns a PDF when xhtml2pdf is installed, otherwise 404."""
    pdf_attachment = True

    def get_pdf_filename(self):
        obj = self.get_object()
        return f'medical-certificate-{obj.unique_number}-{timezone.now():%Y%m%d}.pdf'

    def get(self, request, *args, **kwargs):
        if not XHTML2PDF_AVAILABLE:
            return HttpResponseNotFound(
                'PDF generation is not available on this server. Install xhtml2pdf.'
            )

        # Render the HTML template to a string
        obj = self.get_object()
        context = self.get_context_data(object=obj)
        html = render_to_string(self.template_name, context)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.get_pdf_filename()}"'

        # xhtml2pdf (pisa) writes bytes to response
        result = pisa.CreatePDF(src=html, dest=response)

        if getattr(result, 'err', False):
            return HttpResponse(status=500, content='Error generating PDF')

        return response