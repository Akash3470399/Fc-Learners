from django import forms

from . models import Article

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"id":"content-textarea"}))
    class Meta:
        fields = ('title','category', 'thumbnail', 'content')
        model = Article