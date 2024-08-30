from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name="Dashboard"),
    path('login/', views.login_view, name="Login"),
    path('patientdata/', views.patientdata_view, name="Patient Data"),
    path('patientform-add/', views.patientform_add_view, name="Patient Add")
]