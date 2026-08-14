from django.urls import path

from apps.site import views

app_name = "site"

urlpatterns = [
    path("", views.home, name="home"),
]