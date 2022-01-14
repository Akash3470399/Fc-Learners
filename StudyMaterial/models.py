from os import times
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
class Resource(models.Model):
    choices = (
        ("FY", "FY"),
        ("SY", "SY"),
        ("TY", "TY")
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(upload_to="Study_Material/files")
    title = models.CharField(max_length=150, blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    year = models.CharField(choices=choices, max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True)