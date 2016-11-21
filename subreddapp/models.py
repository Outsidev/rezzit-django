from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    username = models.ForeignKey('auth.User')
    text = models.TextField(default="")
    published_date = models.DateTimeField(default=timezone.now)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Post_Main(Post):
    link_adress = models.CharField(max_length=200)
    title =  models.CharField(max_length=100)

class Post_Comment(Post):
    parent_post = models.ForeignKey('Post_Main')

    def __str__(self):
        return self.text
