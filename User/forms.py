from logging import PlaceHolder
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', "autocomplete":"new-password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password', "autocomplete":"new-password"}))
    class Meta:
        model  = get_user_model()
        fields = ['email', 'name', 'password1', 'password2']

        widgets = {
            'email':forms.EmailInput(attrs={'placeholder':'email', 'id':'user_email'}),
            'name':forms.TextInput(attrs={'placeholder':'name'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))