from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    context = {'posts': page_posts}
    context = {'posts': page_posts, 'page_name': 'All Posts'}
    return render(request, "network/index.html", context)


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def create_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(id=request.user.id)
        post = Post(author=user, content=content)
        post.save()
    return HttpResponseRedirect(reverse(index))


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(author=user).order_by('-timestamp')
    followers = Follow.objects.filter(user=user)
    following = Follow.objects.filter(follower=user)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    requester = request.user.id
    relationship = 'none'

    if requester == user_id:
        relationship = 'owner'
    # elif Follow.objects.filter(user=user, follower=request.user).exists():
    #     relationship = 'following'
    # using reverse relation!
    elif user.followers.filter(follower=request.user).exists():
        relationship = 'following'
    elif user.following.filter(user=request.user).exists():
        relationship = 'followed'

    context = {'posts': page_posts,
               'user_id': user_id,
               'page_name': user.username + " Posts",
               'reg_date': user.registration_date.strftime("%B %Y "),
               'followers': followers,
               'following': following,
               'relationship': relationship, }
    return render(request, "network/profile.html", context)


def handle_follow_action(requester_id, user_id, action):
    requester = User.objects.get(id=requester_id)
    user = User.objects.get(id=user_id)
    if action == "Unfollow":
        follow_process = Follow.objects.get(user=user, follower=requester)
        follow_process.delete()
    else:
        follow_process = Follow(user=user, follower=requester)
        follow_process.save()


def follow(request):
    if request.method == "POST":
        requester = request.user.id
        user_to_relate = request.POST["user"]
        action = request.POST["action"]

        handle_follow_action(request.user.id, user_to_relate, action)
    return profile(request, user_to_relate)


def following(request):
    requester = request.user
    followings = requester.following.all()
    following_users = [followings.user for followings in followings]

    posts=[]
    for user in following_users:
        user_posts = user.post.all()
        posts.append(user_posts)

    flattened_posts = [post for sublist in posts for post in sublist]
    sorted_posts = sorted(flattened_posts, key=lambda post: post.timestamp, reverse=True)

    paginator = Paginator(sorted_posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    context = {'posts': page_posts}
    context = {'posts': page_posts, 'page_name': 'Following Posts'}
    return render(request, "network/index.html", context)