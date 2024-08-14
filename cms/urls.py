from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('login/', views.login_view, name="Login"),
]