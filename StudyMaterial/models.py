from os import times
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Resource(models.Model):
    choices = (
        ("FY", ("FY")),
        ("SY", ("SY")),
        ("TY", ("TY"))
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="Study_Material/files")
    subject = models.CharField(max_length=100, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    year = models.CharField(choices=choices, max_length=5)