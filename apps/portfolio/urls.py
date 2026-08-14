from django.urls import path

from apps.portfolio import views

app_name = "portfolio"

urlpatterns = [
    path("portafolio/", views.portfolio_project_list, name="list"),
    path("portafolio/<slug:business_slug>/", views.portfolio_project_business_list, name="business_list"),
    path("portafolio/<slug:business_slug>/<slug:project_slug>/", views.portfolio_project_detail, name="detail"),
]