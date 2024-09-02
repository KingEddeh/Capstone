from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name="Dashboard"),
    path('login/', views.login_view, name="Login"),
    path('patientdata/', views.patientdata_view, name="Patient Data"),
    path('patientform-add/', views.patientform_add_view, name="Patient Add"),
    path('patientform-update/<str:pk>/', views.patientform_update_view, name="Patient Update"),
    path('patientform-delete/<str:pk>/', views.patientform_delete_view, name="Patient Delete")
]