from django.urls import path

from apps.contact import views

app_name = "contact"

urlpatterns = [
    path("contacto/", views.contact_form, name="form"),
    path("contacto/enviado/", views.contact_success, name="success"),
]