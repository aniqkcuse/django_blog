from django.db import models
from users.models import CustomUser

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    vote = models.IntegerField(default=0)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.content} - {self.article.title}" 

class Blog(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"Article: {self.article.title}"
    
class UserVoteArticle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.article} - {self.is_voted}"

class UserVoteCommentary(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    commentary = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.commentary} - {self.is_voted}"