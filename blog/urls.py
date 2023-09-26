from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("article/<int:pk>", views.articles, name="blog_article"),
    path("blog/<int:pk>", views.blog_view, name="blog_blog"),
    path("article/create/", views.article_create, name="blog_article_create"),
    path("article/update/<int:pk>", views.article_update, name="blog_article_update"),
    path("article/delete/<int:pk>", views.article_delete, name="blog_article_delete"),
    path("article/update/commentary/<int:pk>", views.update_commentary, name="blog_commentary_update"),
    path("article/delete/comentary/<int:pk>", views.delete_comentary, name="blog_commentary_delete"),
    path("article/upvote/<int:pk>", views.upvote_article, name="blog_article_upvote"),
    path("article/downvote/<int:pk>", views.downvote_article, name="blog_article_downvote"),
    path("article/upvote/commentary/<int:pk>", views.upvote_commentary, name="blog_commentary_upvote"),
    path("article/downvote/comentary/<int:pk>", views.downvote_commentary, name="blog_commentary_downvote"),
    path("", RedirectView.as_view(url="blog/0"))
]
