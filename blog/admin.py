from django.contrib import admin
from .models import Blog, Article, Comment, UserVoteArticle, UserVoteCommentary

# Register your models here.
admin.site.register([Blog, Article, Comment, UserVoteArticle, UserVoteCommentary])