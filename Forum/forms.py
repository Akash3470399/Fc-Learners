from dataclasses import fields
from importlib.metadata import files
from django import forms

from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"