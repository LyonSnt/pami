from django.urls import path

from apps.businesses import views

app_name = "businesses"

urlpatterns = [
    path("negocios/", views.business_list, name="list"),
    path("negocios/<slug:slug>/", views.business_detail, name="detail"),
]