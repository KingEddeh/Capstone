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
    path('medcertform-export/', views.medcertform_export_view, name="Medcert Export")


    #Inventory--------------------------------------------------------------
]