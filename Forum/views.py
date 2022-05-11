import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Question 
from .forms import QuestionForm, AnswerForm

# Create your views here.
def forum_home(request):
    qustions = Question.objects.all()
    if qustions.count() > 10:
        qustions = qustions[:10]

    context = {'questions':qustions}
    return render(request, "Forum/forum.html", context)

@login_required
def get_question(request, pk):
    question = Question.objects.get(pk = pk)
    try:
        answers = question.answer_set.all()
    except:
        answers = None
    return render(request, "Forum/forum_single.html", {'question':question, 'answers':answers})

@login_required
def add_question(request):
    if request.method == 'POST':
        data = request.POST['content']
        question = {
            'user':request.user,
            'description':data,
            'is_answered':False
        }
        form = QuestionForm(data = question)
        if form.is_valid():
            q = form.save()
            return redirect("Forum:get_question", q.id)
        return redirect("Forum:forum_home")
    else:
        return render(request, "Forum/add_new_question.html")


@login_required
def add_answer(request, pk):
    if request.method == "POST":
        data = request.POST['content']
        print(data)
        answer = {
            'question':Question.objects.get(pk = pk),
            'user' : request.user,
            'answer_text': data
        }

        form = AnswerForm(data = answer)
        if form.is_valid():
            form.save()
            return redirect("Forum:get_question", pk)
    return render(request, "Forum/add_new_answer.html", {'question_no':pk})