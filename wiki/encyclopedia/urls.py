from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.Entry_Page, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new_page, name="new"),
    path("save", views.save, name="save"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save_edit", views.save_edit, name="save edit"),
    path("random", views.random_page, name="random")
    ]
