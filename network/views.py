from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PostForm
from .models import Posts, Profile
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import random


# Get all posts and dispaly them to the screen 10 at a time
def index(request):
    # Get all posts ordered by time posted
    all_posts = Posts.objects.all().order_by('-time_posted')

    # Create paginator to display 10 at a time
    p = Paginator(all_posts, 10)
    page = request.GET.get('page')
    all_posts_paginated = p.get_page(page)

    # if user is logged in get a random quote
    if request.user.is_authenticated:
        quotes = ['Penny for your thoughts.',
                  'Express your thoughts.',
                  'What\'s on your mind?',
                  'What are you thinking?',
                  'Say something.',
                  'Share your ideas.',
                  ]
        quote = random.choice(quotes)

        # Display the index page with the post form and
        # random quote
        return render(request, "network/index.html", {
            "all_posts": all_posts_paginated,
            "post_form": PostForm(),
            "quote": quote
        })
    # If user is not signed in, display all posts but don't
    # display a form
    else:
        return render(request, "network/index.html", {
            "all_posts": all_posts_paginated,
            "quote": "User is not authenticated."
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


# Get contents of new post text
def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        # If form is valid add a row to the posts table
        if form.is_valid():
            post = form.cleaned_data["post"]
            new_post = Posts(user=request.user, post=post)
            new_post.save()

    # If user did not make a "POST" request, go to index page
    return HttpResponseRedirect(reverse("index"))


# Used to get information for the user's profile page
def profile(request, user):
    # Bolean 'can_follow' is used to make sure user doesn't follow themselves
    can_follow = False
    follow_status = 'Follow'
    user_id = User.objects.get(username=user)

    if request.user.is_authenticated:
        # Get the profile of the current logged in user
        request_user_id = User.objects.get(username=request.user)
        profile = Profile.objects.get(profile=request_user_id)

        # If user already follows display 'unfollow'
        if user_id in profile.follows.all():
            follow_status = 'Unfollow'
        # If current logged in user is not visiting their
        # own profile page, then display the follow button
        if str(request.user) != user:
            can_follow = True

    # Get all posts, following count, and follwer count for the profile
    all_posts = Posts.objects.filter(user=user_id).order_by('-time_posted')
    total_followers = Profile.objects.filter(follows=user_id).count()
    total_followees = Profile.objects.get(profile=user_id).follows.count()

    # Paginator do display 10 posts at a time
    p = Paginator(all_posts, 10)
    page = request.GET.get('page')
    all_posts_paginated = p.get_page(page)

    # Display the profile with associated values/variables
    return render(request, "network/profile.html", {
        'can_follow': can_follow,
        'all_posts': all_posts_paginated,
        'profile_user': user,
        'follow_status': follow_status,
        'total_followers': total_followers,
        'total_followees': total_followees
    })


# Add or remove user from following table
def follow(request, user):
    request_user_id = User.objects.get(username=request.user)
    user_id = User.objects.get(username=user)
    profile = Profile.objects.get(profile=request_user_id)

    if user_id in profile.follows.all():
        # Removed user from the follow list
        profile.follows.remove(user_id)
    else:
        # Added usuer to the follow list
        profile.follows.add(user_id)

    # Update profile and redirect back to profile page
    profile.save()
    return redirect('profile', user)


# Get all posts from only the user that the logged in
# user currently follows
def following(request):
    # Only users who are logged in have a following list
    if request.user.is_authenticated:
        # Get all users that are in the current logged in users profile
        user_id = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(profile=user_id)
        all_follows = user_profile.follows.all()

        # Get all posts from the following users, ordered by time
        all_posts = Posts.objects.filter(
            user__in=all_follows).order_by("-time_posted")

        # Paginator to display 10 at a time
        p = Paginator(all_posts, 10)
        page = request.GET.get('page')
        all_posts_paginated = p.get_page(page)

        # Display all posts from following list
        return render(request, "network/following.html", {
            "all_posts": all_posts_paginated,
        })
    # If user is not logged in, display a message
    else:
        return HttpResponse("Please log in to view posts from users that you follow.")


# Used to update text from a post
@csrf_exempt
def edit(request):
    data = json.loads(request.body)
    new_text = data['post']
    post = Posts.objects.get(id=data['id'])

    # Ensures user can only edit their own posts
    if request.user.username == post.user.username:
        # update the post with new text and save
        post.post = new_text
        post.save()
        return JsonResponse({"outcome": "Success"})
    # If user tries to edit someone else's post
    return JsonResponse({"outcome": "Failure"})


# Used to update the like count for a post
@csrf_exempt
def like(request):
    data = json.loads(request.body)
    post = Posts.objects.get(id=data['id'])
    user_id = User.objects.get(username=request.user)

    # Check to see if user is already liking this post
    if user_id in post.likes.all():
        # If user already liking, then remove from likes
        post.likes.remove(user_id)
        post.save()
        return JsonResponse({"outcome": "Removed"})

    # If user is not in the post's likes then
    # add user to likes
    post.likes.add(user_id)
    post.save()
    return JsonResponse({"outcome": "Added"})
