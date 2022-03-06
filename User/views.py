import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout



from .models import CustomUser
from .forms import UserRegisterForm, UserLoginForm


def register_or_login(request):
    context = {'registerform':UserRegisterForm(), 'loginform':UserLoginForm()}
    return render(request, 'User/login_signup.html', context)


def user_register(request):
    if request.method == 'POST':
        json_data = json.load(request)
        if(json_data['email'].endswith("fc.com")):
            json_data['is_teacher'] = True
            
        form = UserRegisterForm(data=json_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'},)
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
                return JsonResponse({'status':'success'},)
            else:
                err = ""
                user = CustomUser.objects.filter(email=data['email'])
                if not user.exists():
                    err = {'email' :"User not found."}
                else:
                    err = {'password' :"Invalid password."}
                return JsonResponse({'status':'fail', 'errors':err})
        else:
            return JsonResponse({'status':'fail', 'errors':form.errors})

def logout_user(request):
    logout(request)
    return redirect('Blog:blog_home')


def student_dash(request):
    if not request.user.is_authenticated:
        return redirect('User:register_or_login')
    user=CustomUser.objects.get(id=request.user.id)
    d={'user':user}
    return render(request, 'User/student_dash.html',d)

def teacher_dash(request):
    if not request.user.is_authenticated:
        return redirect('User:register_or_login')
    user=CustomUser.objects.get(id=request.user.id)
    d={'user':user}
    return render(request, 'User/teacher_dash.html',d)