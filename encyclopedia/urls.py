from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("random", views.randompage, name="random"),
    path("<str:title>", views.entry, name="entry"),
]