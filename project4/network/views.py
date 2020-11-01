from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from json import dumps 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from .models import User, posts, follow, likes


def index(request):
    all_posts = posts.objects.all()
    all_posts = all_posts.order_by("-timestamp").all()

    no_posts = all_posts.count()
    all_posts = paginate(request, all_posts)

    
    return render(request, "network/index.html",{
        "posts": all_posts,
        "no_posts":no_posts,
        "title":"All Posts"
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            follow_info= follow(user = user, no_followers=0, no_following=0)
            follow_info.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def posting(request):
    content = request.GET.get('content')
    post = posts(user = request.user, content = content, no_likes = 0)
    post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def edit(request, id):
    data = json.loads(request.body)
    post = posts.objects.get(pk=id)
    post.content = data['content']
    post.save()
    return JsonResponse({"message": "post edited successfully."}, status=201)


@csrf_exempt
@login_required
def like(request, id):

    liked_post = posts.objects.get(pk = id)
    x = likes.objects.filter(user=request.user, post=liked_post)

    if(x.exists()):
        liked_post.no_likes -= 1

        x.delete()
        liked_post.save()

        return JsonResponse({"no_likes": liked_post.no_likes}, safe= False)
    else:
        new_like = likes(user = request.user, post= liked_post)

        liked_post.no_likes += 1
        
        new_like.save()
        liked_post.save()

        return JsonResponse({"no_likes": liked_post.no_likes,
                            "exists": x.exists()}, safe= False)


def does_like(request):

     
    liked_posts = likes.objects.filter(user=request.user)
    liked_posts.order_by("-posts__timestamp")

    all_posts = posts.objects.all()
    all_posts = all_posts.order_by("-timestamp").all()
    
    return JsonResponse([like.serialize() for like in liked_posts], safe= False)




def profile(request, user):
    all_posts = posts.objects.filter(user=user)
    all_posts = all_posts.order_by("-timestamp").all()
    follow_info = follow.objects.filter(user=user).last()

    no_posts = all_posts.count()
    all_posts = paginate(request, all_posts)

    return render(request, "network/profile.html",{
    "posts": all_posts,
    "no_posts":no_posts,
    "follow": follow_info,
    "no_following":follow.objects.values("following").filter(user = user).count() - 1,
    "no_followers":follow.objects.values("following").filter(following = user).count(),

    })


@login_required
def following(request):
    followings =  follow.objects.values_list("following",flat=True).filter(user = request.user)

    all_posts = posts.objects.filter(user__id__in = followings)
    all_posts = all_posts.order_by("-timestamp").all()

    no_posts = all_posts.count()
    all_posts = paginate(request, all_posts)

    return render(request, "network/index.html",{
        "posts":all_posts,
        "no_posts":no_posts,
        "title":"Following"
    })

@csrf_exempt
@login_required
def follows(request, id):

    if(follow.objects.filter(user = request.user, following =   id).exists()):

        d1 = follow.objects.filter(user = request.user, following =  id).first()
        d1.delete()
        return JsonResponse({"is_following":[j1.serialize() for j1 in follow.objects.filter(user = request.user, following = id)],
                            "no_followers":[j2.serialize() for j2 in follow.objects.filter(following = id)]}, safe=False)
    else:
        f1 = follow(user = request.user, following = follow.objects.filter(user = id).first().user)
        f1.save()
        return JsonResponse({"is_following":[j1.serialize() for j1 in follow.objects.filter(user = request.user, following = id)],
                            "no_followers":[j2.serialize() for j2 in follow.objects.filter(following = id)]}, safe=False)


def does_follow(request, id):
    return JsonResponse({"is_following":[j1.serialize() for j1 in follow.objects.filter(user = request.user, following = id)]})


def paginate(request, all_posts):
    paginator = Paginator(all_posts, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def getUsername(request):
    if request.user.is_authenticated :
        username =  request.user.username
       
        return username


