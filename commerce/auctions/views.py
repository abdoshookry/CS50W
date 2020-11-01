from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from .models import auction_listings, comments, bid, watchlists


def index(request):
    return render(request, "auctions/index.html", {
        "listings": auction_listings.objects.filter(closed=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    return render(request, "auctions/create.html",{
        "form":listing_form()
    })


class listing_form(forms.Form):
    name = forms.CharField(max_length=64, widget= forms.TextInput(
        attrs={
            'placeholder': "(required)"
            }
        ))
    descreption = forms.CharField(max_length=500, widget= forms.Textarea(
        attrs={
            'placeholder': "(required)"
            }
        ))
    bid = forms.CharField( widget= forms.TextInput(
        attrs={
            'placeholder': "(required)"
            }
        ))
    image = forms.URLField(required=False, widget= forms.TextInput(
        attrs={
            'placeholder': "(optional)"
            }
        ))
    category = forms.CharField(max_length=64, required=False, widget= forms.TextInput(
        attrs={
            'placeholder': "(optional)"
            }
        ))


def save_listing(request):
    try:  
        username = None
        if User.is_authenticated:
            username = request.user.username
        
            price = bid(price = request.POST["bid"])
            price.save()

            watchlist = watchlists(is_watching=False)
            watchlist.save()
            

            listing = auction_listings(name = request.POST["name"], 
            descreption = request.POST["descreption"], 
            bid = price ,
            image = request.POST["image"],
            category = request.POST["category"],
            author = username,
            watchlists = watchlist)
        
            listing.save()

            return HttpResponseRedirect(reverse("index"))
    except:
        return HttpResponseRedirect(reverse("error"))
    


def listing(request, id):
    try: 
        listing = auction_listings.objects.get(pk=id)

        author = isAuthor(request, listing)

        return render(request, "auctions/listing.html",{
            "listing":auction_listings.objects.get(pk = id),
            "author":author,
            "comments": listing.comments.all()

        })
    except:
        return HttpResponseRedirect(reverse("error", args=(id,)))

def biding(request, id):
    try: 
        if request.user.is_authenticated :
            bid = int(request.POST["bid"])
            listing = auction_listings.objects.get(pk=id)

            author = isAuthor(request, listing)
            username = getUsername(request)

            if listing.bid.price < bid or (listing.bid.price == bid and listing.bid.highestBid==""):
                listing.bid.price = bid
                listing.bid.save()

                listing.bid.highestBid = username
                listing.bid.save()

                return HttpResponseRedirect(reverse("bid saved", args=(id,)))
            
            else:
                return  HttpResponseRedirect(reverse("bid failed", args=(id,)))
        else:
            return HttpResponseRedirect(reverse("signin_error"))
    except:
        HttpResponseRedirect(reverse("error"))

def bid_saved(request, id):
    return render(request, "auctions/bid.html",{
    "message":"bid completed successfully",
    "id":id
    })
def bid_failed(request, id):
    return render(request, "auctions/bid.html",{
        "message":"error : the bid must be bigger than the current highest bid",
        "id":id
        })
    

def comment(request, id):
    listing = auction_listings.objects.get(pk= id)

    comment = comments(text = request.POST["comment"], commenter = getUsername(request))
    comment.save()

    listing.comments.add(comment)
    listing.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def add_watchlist(request, id):
    if request.user.is_authenticated :
        listing = auction_listings.objects.get(pk = id)

        listing.watchlists.is_watching = True
        listing.watchlists.save()

        listing.watchlists.user = getUsername(request)
        listing.watchlists.save()


        return HttpResponseRedirect(reverse("watchlist"))
    else:
        return HttpResponseRedirect(reverse("signin_error"))

def remove_watchlist(request, id):
    if request.user.is_authenticated :
        listing = auction_listings.objects.get(pk = id)
        listing.watchlists.is_watching = False
        listing.watchlists.save()

        listing.watchlists.user = getUsername(request)
        listing.watchlists.save()

        return HttpResponseRedirect(reverse("watchlist"))
    else:
        return HttpResponseRedirect(reverse("signin_error"))
    
def watchlist(request):

    return render (request, "auctions/watchlist.html",{
        "listings":auction_listings.objects.filter(watchlists__is_watching = True, watchlists__user = getUsername(request))

    })


def close(request, id):

    listing = auction_listings.objects.get(pk=id)
    listing.closed=True
    listing.save()
    
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "comments":listing.comments.all(),
        "author":isAuthor(request,listing)
    })
def closed(request):
    return render (request, "auctions/closed.html",{
        "listings":auction_listings.objects.filter(closed=True)

    })


def categories(request):
    categories = auction_listings.objects.values("category").filter(closed=False).distinct()
    return render(request, "auctions/categories.html",{
        "categories": categories.all()
    })

def category(request, category):
    if category == "no category":
        category =""
    return render(request, "auctions/category.html",{
        "listings": auction_listings.objects.filter(closed=False, category=category),
        "category":category
    })

def signin_error(request):
    return render(request, "auctions/signin_error.html")

def error(request, id = None):
    if id == None:
        return render(request, "auctions/error.html")
    else:
        return render(request, "auctions/error.html",{
            "message":"this page doesn\'t exist"
        })

def isAuthor(request, listing):
    if request.user.is_authenticated :
        username = getUsername(request)

        author = False
        if listing.author == username:
            author = True

        return author
    else:
        return False

def getUsername(request):
    if request.user.is_authenticated :
        username =  request.user.username
       
        return username
   



