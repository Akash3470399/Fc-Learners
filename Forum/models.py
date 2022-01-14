from django.db import models
from django.contrib.auth import get_user_model

class Question(models.Model):
    description = models.CharField(max_length=500, blank=False, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    is_answered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.description

class QuestionCategory(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.category
        
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    answer_text = models.CharField(max_length=150, blank=False, null=False)

    def __str__(self) -> str:
        return self.answer_text

class AnswerComment(models.Model):
    Answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=200, blank=False, null= False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment_text
    