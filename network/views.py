from ast import arg
import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PostForm
from .models import Posts, Profile


from .models import User

# TODO make sure to delete one index definition (currently 2 exist)


# def index(request):
#    return render(request, "network/index.html")


def index(request):
    all_posts = Posts.objects.all().order_by('-time_posted')
    if request.user.is_authenticated:
        return render(request, "network/index.html", {
            "all_posts": all_posts,
            "post_form": PostForm(),
            "test": "User is signed in.",
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
    can_follow = True
    user_id = User.objects.get(username=user)
    all_posts = Posts.objects.filter(user=user_id)

    if str(request.user) == user:
        can_follow = False
    return render(request, "network/profile.html", {
        'can_follow': can_follow,
        'all_posts': all_posts,
        'user': user,
        'follow_status': 'follow'
    })


def follow(request, user):
    request_user_id = User.objects.get(username=request.user)
    print(request_user_id)
    profile = Profile.objects.get(profile=request_user_id)
    # TODO
    # Add the user to the users profiles followee's
    print(profile)
    return redirect('profile', user)
