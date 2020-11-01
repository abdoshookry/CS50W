from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("save", views.save_listing, name="save listing"),
    path("watchlist", views.watchlist, name ="watchlist"),
    path("closed", views.closed, name="closed"),
    path("error/<str:id>", views.error, name="error"),
    path("error", views.error, name="error"),
    path("signin/error", views.signin_error, name="signin_error"),
    path("categories", views.categories, name = "categories"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("bid/<str:id>", views.biding, name="bid"),
    path("closed/<str:id>", views.close, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("done/<str:id>", views.bid_saved, name="bid saved"),
    path("failed/<str:id>", views.bid_failed, name="bid failed"),
    path("add/<str:id>", views.add_watchlist, name = "add to watchlist"), 
    path("remove/<str:id>", views.remove_watchlist, name="remove from watchlist"),
    path("category/<str:category>", views.category, name = "category")
    
]
