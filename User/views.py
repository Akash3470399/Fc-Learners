from importlib import resources
from importlib.resources import contents
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage  



from .models import CustomUser
from .forms import UserRegisterForm, UserLoginForm

from Blog.models import Article
from StudyMaterial.models import Resource

blog_paginate_by = 1
notes_paginate_by = 1


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

@login_required
def student_dash(request):
    blogs = request.user.article_set.all()
    blog_paginator = Paginator(blogs, blog_paginate_by)
    blog_page_obj = blog_paginator.get_page(1)
    notes = request.user.resource_set.all().order_by("-timestamp")
    total_count = notes.count()
    pending_count = notes.filter(status="Pending").count()
    notes_paginator = Paginator(notes, notes_paginate_by)
    notes_page_obj = notes_paginator.get_page(1)
    context = {"blog_page":blog_page_obj, "notes_page":notes_page_obj, "pending":pending_count, "total_count":total_count}
    return render(request, 'User/student_dash.html', context)

def teacher_dash(request):
    if not request.user.is_authenticated:
        return redirect('User:register_or_login')
    resouces = Resource.objects.filter(status = "Pending")
    contents = {'resources': resouces}
    return render(request, 'User/teacher_dash.html', contents)


# function to get paginated blog names
@login_required
def paginated_blog_list(request):
    try:
        blogs = request.user.article_set.all()
        paginator = Paginator(blogs, blog_paginate_by)
        if "page" in request.GET:
            page_num = request.GET.get("page")
        else:
            page_num = 1

        page_obj = paginator.get_page(page_num)
        blogs_list = []
        next_page_num = False
        for blog in page_obj.object_list: # createing list of blog information
            blogs_list.append([blog.id, blog.title, blog.category, blog.likes.count(), blog.articlecomment_set.count()])
        if page_obj.has_next():
            next_page_num = page_obj.next_page_number()
            
        res = {'status':"success" ,"blogs_list":blogs_list , "next_page_num":next_page_num}
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"status":"fail"})

# function to get paginated study material details
def paginated_notes_list(request):
    try:
        notes = request.user.resource_set.all().order_by("-timestamp")
        paginator = Paginator(notes, notes_paginate_by)
        if "page" in  request.GET:
            page_num = request.GET.get("page")
        else:
            page_num = 0
        page_obj = paginator.get_page(page_num)
        next_page_num = False
        if page_obj.has_next():
            next_page_num = page_obj.next_page_number()
        notes_list = []
        for note in page_obj:
            n = {
                'id': note.id,
                'title' : note.title, 
                'subject': note.subject,
                'status' : note.status
            }
            notes_list.append(n)
        res = {"status":"success", "notes_list":notes_list, "next_page_num":next_page_num}
        return JsonResponse(res)
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail'})



        
def user_register_with_email(request):
    if request.method == 'POST':
        json_data = json.load(request)
        if(json_data['email'].endswith("fc.com")):
            json_data['is_teacher'] = True
            
        form = UserRegisterForm(data=json_data)
        if form.is_valid():
            user = form.save(commit= False)

            user.is_active = False
            user.save()

            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('User/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  

            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  

            return JsonResponse({'status':'success'},)
        else:
            return JsonResponse({'status':'fail', 'errors':form.errors})
    return redirect("User:register_or_login")


def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse(f'Thank you for your email confirmation. Now you can login your account.<a href={reverse("User:register_or_login")}>Login</a>')  
    else:  
        return HttpResponse('Activation link is invalid!')


def about_us(request):
    return render(request, "User/about_us.html")