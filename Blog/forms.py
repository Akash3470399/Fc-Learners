from django import forms

from . models import Article, TinyEditorImages

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea())
    class Meta:
        fields = ('title','category', 'thumbnail', 'content')
        model = Article

        widgetes = {
            'title': forms.TextInput(attrs={'placeholder':"Title",}),
            'category': forms.TextInput(attrs={'placeholder':"Category",}),
        }

class TinyEditorImagesForm(forms.ModelForm):
    class Meta:
        model = TinyEditorImages
        fields = "__all__"