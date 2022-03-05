from django import forms

from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'subject', 'file', 'description']

        # widget = {
        #     'title': forms.TextInput(attrs={"placeholder": "Title"}),
        #     'subject':forms.TextInput(attrs={'placeholder':"Subject"}),
        #     'description':forms.TextInput(attrs={'placeholder':'Description'})
        # }