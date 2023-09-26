from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import UserCreationForm, UserAuntheticateForm
from blog.models import UserVoteArticle, UserVoteCommentary, Article, Comment

import re

# Create your views here.
def login_user(request):
    if request.method == "GET":
        return render(request, 'user/login.html', {'form':UserAuntheticateForm})
    else:
        user = authenticate(request, email=request.POST["email"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect("blog_blog", 0)
        else:
            return render(request, 'user/login.html', {'form':UserAuntheticateForm, "error":"Error in the login. Please, try again"})
        
@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("blog_blog", 0)

def register_user(request):
    if request.method == "GET":
        return render(request, 'user/register.html', {'form':UserCreationForm})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            password_valid = re.compile(r"[\w(*,$,^,!,*,@,#,%,&,/,=,_,-,)]{6,30}")
            if password_valid.match(request.POST["password1"]) == None:
                return render(request, 'user/register.html', {"form":UserCreationForm, "error":"Password insecure. Please, at least using 6 character"})
            else:
                user = form.save()
                articles = Article.objects.all()
                comments = Comment.objects.all()
                for article in articles:
                    UserVoteArticle.objects.create(user=user, article=article)
                for comment in comments:
                    UserVoteCommentary.objects.create(user=user, commentary=comment)
                login(request, user)

                return redirect("blog_blog", 0)
        else:
            if request.POST["password1"] != request.POST["password2"]:
                return render(request, 'user/register.html', {"form":UserCreationForm, "error":"Password doesn't math, try again"})
            try:
                if CustomUser.objects.get(email=request.POST["email"]):
                    return render(request, 'user/register.html', {"form":UserCreationForm, "error":"Email used, try with another"})
            except:
                    return render(request, 'user/register.html', {"form":UserCreationForm, "error":"Error with email, verify it"})
