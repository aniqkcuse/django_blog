from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Blog, Article, Comment, UserVoteArticle, UserVoteCommentary
from users.models import CustomUser
from .forms import ArticleForm, CommentForm

# Create your views here.
def articles(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = Article.objects.get(id=pk)
            comment.save()
            for user in CustomUser.objects.all():
                UserVoteCommentary.objects.create(user=user, commentary=comment).save()
            return redirect("blog_article", pk)
    else:
        if request.user.is_authenticated == True:
            article = get_object_or_404(Article, id=pk)
            comments = Comment.objects.filter(article_id=pk).order_by("-vote")
            user_vote_article = UserVoteArticle.objects.get(Q(user=request.user), Q(article=article))
            user_vote_commentary = UserVoteCommentary.objects.filter(user__id=request.user.id, commentary__article__id=article.id)
            return render(request, 'blog/article.html', {'article':article, 'comments':comments, 'comment_form':CommentForm, "user_vote_article":user_vote_article, "user_vote_commentary":user_vote_commentary})
        else:
            article = get_object_or_404(Article, id=pk)
            comments = Comment.objects.filter(article_id=pk).order_by("-vote")
            return render(request, 'blog/article.html', {'article':article, 'comments':comments, 'comment_form':CommentForm})
        
def blog_view(request, pk):
    blogs = Blog.objects.all().order_by("-article__vote", "-article__date_created")[0+10*pk:10+10*pk]
    if pk == 0:
        return render(request, 'blog/blog.html', {'blogs':blogs, 'pk_next':pk+1, 'pk_previous':pk})
    else:
        if len(blogs) >= 10:
            return render(request, 'blog/blog.html', {'blogs':blogs, 'pk_next':pk+1, 'pk_previous':pk-1})
        elif len(blogs) >= 1 and len(blogs) < 10:
            return render(request, 'blog/blog.html', {'blogs':blogs, 'pk_next':pk, 'pk_previous':pk-1})
        else:
            return redirect("blog_blog", 0)

@login_required(login_url="login")
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = CustomUser.objects.get(id=request.user.id)
            article.save()
            new_blog = Blog.objects.create(article=article)
            new_blog.save()
            for user in CustomUser.objects.all():
                UserVoteArticle.objects.create(user=user, article=article).save()
            return redirect("blog_blog", 0)
        return render(request, 'blog/create_article.html', {'form':ArticleForm})
    else:
        return render(request, 'blog/create_article.html', {'form':ArticleForm})

@login_required(login_url="login")    
def article_update(request, pk):
    if request.method == "POST":
        article = Article.objects.get(id=pk)
        form = ArticleForm(request.POST)
        if form.is_valid():
            article.title = request.POST["title"]
            article.content = request.POST["content"]
            article.edited = True
            article.save()
            return redirect("blog_blog", 0)
    else:
        article = Article.objects.get(id=pk)
        form = ArticleForm(initial={"title":f"{article.title}", "content":f"{article.content}"})
        return render(request, 'blog/update_article.html', {'form':form, "article":article})

@login_required(login_url="login")    
def article_delete(request, pk):
    article = Article.objects.get(id=pk)
    if request.user.id == article.author.id:
        article.delete()
        return redirect("blog_blog", 0)
    else:
        return redirect("blog_blog", 0)

@login_required(login_url="login")
def update_commentary(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.get(id=pk)
            comment.content = request.POST["content"]
            comment.edited = True
            comment.save()
            return redirect("blog_article", comment.article.id)
    else:
        comment = Comment.objects.get(id=pk)
        form = CommentForm(initial={"content":f"{comment.content}"})
        return render(request, "blog/update_commentary.html", {'form':form, 'comment':comment})

@login_required(login_url="login")
def delete_comentary(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user.id == comment.user.id:
        comment.delete()
        return redirect("blog_article", comment.article.id)
    else:
        return redirect("blog_article", comment.article.id)

@login_required(login_url="login")
def upvote_article(request, pk):
    article = Article.objects.get(id=pk)
    is_voted_user = UserVoteArticle.objects.get(Q(user=request.user.id), Q(article=article.id))
    if is_voted_user.is_voted == True:
        return redirect("blog_article", pk)
    else:
        article.vote += 1
        article.save()
        is_voted_user.is_voted = True
        is_voted_user.save()
        return redirect("blog_article", pk)

@login_required(login_url="login")
def downvote_article(request, pk):
    article = Article.objects.get(id=pk)
    is_voted_user = UserVoteArticle.objects.get(Q(user=request.user.id), Q(article=article.id))
    if is_voted_user.is_voted == True:
        return redirect("blog_article", pk)
    else:
        article.vote -= 1
        article.save()
        is_voted_user.is_voted = True
        is_voted_user.save()
        return redirect("blog_article", pk)

@login_required(login_url="login")
def upvote_commentary(request, pk):
    comment = Comment.objects.get(id=pk)
    is_voted_user = UserVoteCommentary.objects.get(Q(user=request.user.id), Q(commentary=comment.id))
    if is_voted_user.is_voted == True:
        return redirect("blog_article", comment.article.id)
    else:
        comment.vote += 1
        comment.save()
        is_voted_user.is_voted = True
        is_voted_user.save()
        return redirect("blog_article", comment.article.id)

@login_required(login_url="login")
def downvote_commentary(request, pk):
    comment = Comment.objects.get(id=pk)
    is_voted_user = UserVoteCommentary.objects.get(Q(user=request.user.id), Q(commentary=comment.id))
    if is_voted_user.is_voted == True:
        return redirect("blog_article", comment.article.id)
    else:
        comment.vote -= 1
        comment.save()
        is_voted_user.is_voted = True
        is_voted_user.save()
        return redirect("blog_article", comment.article.id)