from django.urls import path

from apps.blog import views

app_name = "blog"

urlpatterns = [
    path("blog/", views.blog_post_list, name="list"),
    path("blog/<slug:slug>/", views.blog_post_detail, name="detail"),
]