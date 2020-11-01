
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("post", views.posting, name = "post"),
    path("following", views.following, name = "following"),
    path("profile/<str:user>", views.profile, name = "profile"),
    path("edit/<str:id>", views.edit, name = "edit"),
    path("like/<str:id>", views.like, name = "like"),
    path("does_like",views.does_like, name = "does_like"),
    path("follow/<str:id>",views.follows, name = "follow"),
    path("does_follow/<str:id>", views.does_follow, name = "does_follow")

]
