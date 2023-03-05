from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(posts, 2)
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

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    context = {'posts': page_posts, 'page_name': user.username + " Posts" }
    return render(request, "network/profile.html", context)
