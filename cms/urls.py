from django.urls import include, path

from . import views

urlpatterns = [
    path("select2/", include("django_select2.urls")),
    path('dashboard/', views.dashboard_view, name="Dashboard"),
    path('login/', views.login_view, name="Login"),

    #patient
    path('patientdata/', views.patientdata_view, name="Patient Data"),
    path('patientform-add/', views.patientform_add_view, name="Patient Add"),
    path('patientform-update/<str:pk>/', views.patientform_update_view, name="Patient Update"),
    path('patientform-delete/<str:pk>/', views.patientform_delete_view, name="Patient Delete"),
    path('patientform-export/', views.patientform_export_view, name="Patient Export"),

    #Logbooks----------------------------------------------------------

    #Medcert
    path('medcertdata/', views.medcertdata_view, name="Medcert Data"),
    path('medcertform-add/', views.medcertform_add_view, name="Medcert Add"),
    path('medcertform-update/<str:pk>/', views.medcertform_update_view, name="Medcert Update"),
    path('medcertform-delete/<str:pk>/', views.medcertform_delete_view, name="Medcert Delete"),
    path('medcertform-export/', views.medcertform_export_view, name="Medcert Export"),

    #Referral
    path('referraldata/', views.referraldata_view, name="Referral Data"),
    path('referralform-add/', views.referralform_add_view, name="Referral Add"),
    path('referralform-update/<str:pk>/', views.referralform_update_view, name="Referral Update"),
    path('referralform-delete/<str:pk>/', views.referralform_delete_view, name="Referral Delete"),
    path('referralform-export/', views.referralform_export_view, name="Referral Export"),

    #Treatment
    path('treatmentdata/<str:fk>/', views.treatmentdata_view, name="Treatment Data"),
    path('treatmentform-add/<str:fk>/', views.treatmentform_add_view, name="Treatment Add"),
    path('treatmentform-update/<str:pk>/', views.treatmentform_update_view, name="Treatment Update"),
    path('treatmentform-delete/<str:pk>/', views.treatmentform_delete_view, name="Treatment Delete"),
    path('treatmentform-export/', views.treatmentform_export_view, name="Treatment Export"),

    #Inventory--------------------------------------------------------------
    path('inventorydata/', views.inventorydata_view, name="Inventory Data"),
    path('inventoryform-add/', views.inventoryform_add_view, name="Inventory Add"),
    path('inventoryform-update/<str:pk>/', views.inventoryform_update_view, name="Inventory Update"),
    path('inventoryform-delete/<str:pk>/', views.inventoryform_delete_view, name="Inventory Delete"),
    path('inventoryform-export/', views.inventoryform_export_view, name="Inventory Export"),

    #Medicine
    path('medicinedata/', views.medicinedata_view, name="Medicine Data"),
    path('medicineform-add/', views.medicineform_add_view, name="Medicine Add"),
    path('medicineform-update/<str:pk>/', views.medicineform_update_view, name="Medicine Update"),
    path('medicineform-delete/<str:pk>/', views.medicineform_delete_view, name="Medicine Delete"),
    path('medicineform-export/', views.medicineform_export_view, name="Medicine Export"),

    #Prescription
    path('prescriptiondata/<str:fk>/', views.prescriptiondata_view, name="Prescription Data"),
    path('prescriptionform-add/<int:fk>/', views.prescriptionform_add_view, name="Prescription Add"),
    path('prescriptionform-update/<str:pk>/<str:fk>/', views.prescriptionform_update_view, name="Prescription Update"),
    path('prescriptionform-delete/<str:pk>/<str:fk>/', views.prescriptionform_delete_view, name="Prescription Delete"),
    path('prescriptionform-export/', views.prescriptionform_export_view, name="Prescription Export"),

    #Data Analytics
    path('chart/', views.chart_view, name="chart"),
    path('department-cases-chart/', views.department_cases_view, name='department_cases_chart'),

    #API==============================================================
    path('api/logbooks/', views.get_logbook_data, name="test"),
]