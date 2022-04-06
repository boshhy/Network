from django import http
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PostForm
from .models import Posts, Profile
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json


from .models import User

# TODO make sure to delete one index definition (currently 2 exist)


# def index(request):
#    return render(request, "network/index.html")


def index(request):
    all_posts = Posts.objects.all().order_by('-time_posted')

    p = Paginator(all_posts, 10)
    page = request.GET.get('page')
    all_posts_paginated = p.get_page(page)

    if request.user.is_authenticated:
        return render(request, "network/index.html", {
            "all_posts": all_posts_paginated,
            "post_form": PostForm(),
            "test": "Signed in as " + request.user.username,
        })
    else:
        return render(request, "network/index.html", {
            "all_posts": all_posts,
            "test": "User is not authenticated."
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile(profile=user)
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post(request):
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data["post"]
            new_post = Posts(user=request.user, post=post)
            new_post.save()
    print(user)
    return HttpResponseRedirect(reverse("index"))


def profile(request, user):
    can_follow = False
    follow_status = 'Follow'

    user_id = User.objects.get(username=user)

    if request.user.is_authenticated:
        request_user_id = User.objects.get(username=request.user)
        profile = Profile.objects.get(profile=request_user_id)
        if user_id in profile.follows.all():
            follow_status = 'Unfollow'
        if str(request.user) != user:
            can_follow = True

    all_posts = Posts.objects.filter(user=user_id).order_by('-time_posted')
    total_followers = Profile.objects.filter(follows=user_id).count()
    total_followees = Profile.objects.get(profile=user_id).follows.count()

    p = Paginator(all_posts, 10)
    page = request.GET.get('page')
    all_posts_paginated = p.get_page(page)

    return render(request, "network/profile.html", {
        'can_follow': can_follow,
        'all_posts': all_posts_paginated,
        'profile_user': user,
        'follow_status': follow_status,
        'total_followers': total_followers,
        'total_followees': total_followees
    })


def follow(request, user):
    request_user_id = User.objects.get(username=request.user)
    user_id = User.objects.get(username=user)
    profile = Profile.objects.get(profile=request_user_id)

    if user_id in profile.follows.all():
        print('removed user from follow list')
        profile.follows.remove(user_id)
    else:
        print("added user to follow list")
        profile.follows.add(user_id)

    profile.save()
    return redirect('profile', user)


def following(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(profile=user_id)
        all_follows = user_profile.follows.all()
        all_posts = Posts.objects.filter(
            user__in=all_follows).order_by("-time_posted")
        p = Paginator(all_posts, 10)
        page = request.GET.get('page')
        all_posts_paginated = p.get_page(page)
        return render(request, "network/following.html", {
            "all_posts": all_posts_paginated,
        })

    else:
        return HttpResponse("Please log in to view posts from users that you follow.")


@csrf_exempt
def edit(request):
    data = json.loads(request.body)
    new_text = data['post']
    post = Posts.objects.get(id=data['id'])
    if request.user.username == post.user.username:
        post.post = new_text
        post.save()
        return JsonResponse({"outcome": "Success"})
    return JsonResponse({"outcome": "Failure"})


@csrf_exempt
def like(request):
    data = json.loads(request.body)
    post = Posts.objects.get(id=data['id'])
    user_id = User.objects.get(username=request.user)

    if user_id in post.likes.all():
        post.likes.remove(user_id)
        post.save()
        return JsonResponse({"outcome": "Removed"})

    post.likes.add(user_id)
    post.save()
    return JsonResponse({"outcome": "Added"})
