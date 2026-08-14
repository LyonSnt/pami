from django.urls import path

from apps.catalog import views

app_name = "catalog"

urlpatterns = [
    path("catalogo/", views.product_list, name="list"),
    path("catalogo/<slug:business_slug>/", views.product_business_list, name="business_list"),
    path("catalogo/<slug:business_slug>/<slug:product_slug>/", views.product_detail, name="detail"),
]