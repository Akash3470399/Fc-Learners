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
    latest_notes = Resource.objects.order_by('-timestamp')
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
def add_study_material(request):
    form = ResourceForm()
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            newResouce = form.save(commit=False)
            newResouce.user = request.user
            newResouce.save()
            return redirect("StudyMaterial:study_home")
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
        notes_list = [[note.title, note.file.url] for note in notes]
        res = render_to_string("StudyMaterial/paginated_notes.html", {"notes":notes, "is_paginated":False})
        return JsonResponse({"status":"success", "data":res, "notes_list":notes_list})
    else:
        return JsonResponse({"status":"fail"})


# function to delete a note
@login_required
def delete_note(request, pk):
    try:
        Resource.objects.get(id = pk).delete()
        return JsonResponse({'status':'success'})
    except:
        return JsonResponse({'status':'fail'})
