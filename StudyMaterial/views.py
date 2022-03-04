from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render,redirect

from StudyMaterial .models import Resource
# Create your views here.
 
def index(request):
    return render(request, 'StudyMaterial/Studyhome.html')


def Logout(request):
    logout(request)
    return redirect('study_home')

def study_listing(request):
    return render(request,'StudyMaterial/Studylisting.html')

def get_paginated_material(request):
    notes = Resource.objects.all()
    paginator = Paginator(notes, 1)
    try:
        page_num = request.GET.get("page")
    except:
        page_num = 0
    page_obj = paginator.get_page(page_num)
    
    res = render_to_string("Blog/paginated_notes.html", {'posts':page_obj, 'page_obj':page_obj})
    return JsonResponse({'res':res, 'page_num':page_num, 'total_pages': paginator.num_pages})

# def search_notes(request, q):
#     query_notes = Resource.objects.filter(title__icontains=q)
#     if query_notes.count() > 9:
#         notes = query_notes[:9]
#     else:
#         notes = query_notes
#     res = render_to_string("StudyMaterial/paginated_notes.html", {'notes':notes})

#     result = [[Resource.title, Resource.id] for notes in query_notes]
#     if result:
#         return JsonResponse({'status':'success', 'data':result, 'res':res})
#     return JsonResponse({'status':'fail'})