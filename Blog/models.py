from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to = 'Article/thumbnails/')
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, null=False, blank= False)
    description = models.CharField(max_length=1000, null=False, blank=False)
    likes = models.ManyToManyField(get_user_model(), related_name="post_like")

    def __str__(self) -> str:
        return self.title

class ArticleComment(models.Model):
    Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=500, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text