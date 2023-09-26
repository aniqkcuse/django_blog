from django.forms.models import ModelForm
from .models import Article, Comment

class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class":"form-control"})
        self.fields["content"].widget.attrs.update({"class":"form-control"})

    class Meta:
        model = Article
        fields = ["title","content"]

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update({"class":"form-control"})

    class Meta:
        model = Comment
        fields = ["content"]