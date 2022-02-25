from dataclasses import field, fields
from email.headerregistry import Group
from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


from .forms import UserRegisterForm
from .models import CustomUser

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'about', 'is_active', 'is_admin', 'is_superuser', 'is_teacher')

    def clean_password(self):
        return self.initial['password']

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm #to change user instance
    add_form = UserRegisterForm # to add a user

    list_display = ('email', 'name', 'is_admin', 'about')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'name','password', 'about')
            ),
        }),
        ('Permissions', {
            'fields':('is_admin', 'is_superuser', 'is_active', 'is_staff', 'is_teacher')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('email', 'name', 'about','password1', 'password2'),
        }),
    )
     
    search_fields = ('email','name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)

admin.site.unregister(Group)