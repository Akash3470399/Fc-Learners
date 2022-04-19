from django.shortcuts import render
from .models import Question 

# Create your views here.
def forum_home(request):
    qustions = Question.objects.all()
    if qustions.count() > 10:
        qustions = qustions[:10]

    context = {'questions':qustions}
    return render(request, "Forum/forum.html", context)