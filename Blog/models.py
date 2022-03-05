import datetime
from email.mime import image 
from sqlite3 import Timestamp
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to = 'Article/thumbnails/',default='Article/thumbnails/default.jpg', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200,  null=False, blank= False)
    content = models.CharField(max_length=10000, default="", null=False, blank=False)
    likes = models.ManyToManyField(get_user_model(), related_name="post_like")

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("Blog:blog_detail", kwargs={'pk':self.pk})

    @classmethod
    def get_winners(cls):
        i = 2
        posts = cls.objects.filter(timestamp__date__gte=datetime.date.today() - datetime.timedelta(7))
        while posts.count() < 4 and i < 10:
            posts = cls.objects.filter(timestamp__date__gte=datetime.date.today() -datetime.timedelta(7*i))
            i += 1
        post_like = []
        try:
            # sorting posts w.r.t likes counts
            for post in posts:
                post_like.append([post, post.likes.count(), post.user.id])
            sorted_list = sorted(post_like, key=lambda p:p[1], reverse=True)
            winners = [post[0] for post in sorted_list[:4]]
            del sorted_list
            return winners
        except:
            pass
        
class ArticleComment(models.Model):
    Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=500, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

class TinyEditorImages(models.Model):
    image = models.ImageField(upload_to = "tinyEditor/images/")