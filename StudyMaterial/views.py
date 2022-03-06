from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from StudyMaterial .models import Resource
from User.models import CustomUser
from .forms import ResourceForm
# Create your views here.
 
def index(request):
    latest_notes = Resource.objects.order_by('-timestamp')[:6]
    context = {'latest_notes':latest_notes}
    return render(request, 'StudyMaterial/Studyhome.html',context)



def study_material_listing(request):
    try:
        study_material = Resource.objects.filter(status="Accepted").order_by("-timestamp")
        paginator = Paginator(study_material, 2)
        if "page" in request.GET:
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            res = render_to_string("StudyMaterial/paginated_notes.html", {'notes':page_obj, 'page_obj':page_obj, "is_paginated":True})
            return JsonResponse({'status':'success', 'data':res})
        page_obj = paginator.get_page(1)
        context = {'notes':page_obj, "page_obj":page_obj,"is_paginated":True}
        return render(request,'StudyMaterial/Studylisting.html', context)
    except Exception as e:
        print(e)

@login_required
def add_study(request):
    if not request.user.is_authenticated:
        return redirect('User:register_or_login')
    error=""
    if request.method=='POST':
        t=request.POST['title']
        s=request.POST['subject']
        n=request.FILES['notesfile']
        d=request.POST['description']
        u=CustomUser.objects.filter(name=request.user.name).first()
        try:
            if request.user.is_teacher:
                Resource.objects.create(user=u,file=n,title=t,subject=s,description=d,timestamp=date.today(),status='Accept')
                error="no"
                print(t,s,n,d,u)
            else:
                Resource.objects.create(user=u,file=n,title=t,subject=s,description=d,timestamp=date.today(),status='Pending')
                error="no"
                #print(t,s,n,d,u)
        except:
            error="yes"
            #print(t,s,n,d,u)    
    d={'error':error}
    return render(request,'StudyMaterial/addstudy.html',d)

def add_study_material(request):
    form = ResourceForm()
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            newResouce = form.save(commit=False)
            newResouce.user = request.user
            newResouce.save()
            return redirect("StudyMaterial:study_material_listing")
        else:
            return render('StudyMaterial/addstudy.html', {'form': form})
    return render(request,'StudyMaterial/addstudy.html', {'form': form})


# search notes
def search_notes(request):
    title = request.GET.get('q')
    notes = Resource.objects.filter(title__icontains=title)
    if notes.count() > 9:
        notes = notes[:9]
    if notes:
        res = render_to_string("StudyMaterial/paginated_notes.html", {"notes":notes, "is_paginated":False})
        return JsonResponse({"status":"success", "data":res})
    else:
        return JsonResponse({"status":"fail"})
