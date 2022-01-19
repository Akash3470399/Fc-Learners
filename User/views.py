import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from .models import CustomUser
from .forms import UserRegisterForm, UserLoginForm


def register_or_login(request):
    return render(request, 'User/login_signup.html', {'registerform':UserRegisterForm(), 'loginform':UserLoginForm()})


def user_register(request):
    if request.method == 'POST':
        json_data = json.load(request)
        form = UserRegisterForm(data=json_data)
        if form.is_valid():
            u = form.save()
            return JsonResponse({'status':'success', 'link':reverse("Blog:blog_home")},)
        else:
            return JsonResponse({'status':'fail', 'errors':form.errors})
    return redirect("User:register_or_login")

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data = json.load(request))
        if form.is_valid():
            data = form.data
            user = authenticate(request, email = data['email'], password=data['password'])
            if user is not None:
                login(request, user)
                return JsonResponse({'status':'success', 'link':reverse("Blog:blog_home")},)
            else:
                return JsonResponse({'status':'fail', 'errors':'not authenticated'})
        else:
            return JsonResponse({'status':'fail', 'errors':form.errors})