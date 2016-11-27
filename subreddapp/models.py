from django.db import models
from django.utils import timezone

# Create your models here.

class PostParent(models.Model):
    text = models.TextField(default="")
    published_date = models.DateTimeField(default=timezone.now)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def point_up(self):
        self.points +=1                    
        self.save()    

    def point_down(self):
        self.points -=1                    
        self.save()    


    def __str__(self):
        return self.title

class Post(PostParent):
    username = models.ForeignKey('auth.User', related_name="user_mainposts")
    link_adress = models.CharField(max_length=200)
    title =  models.CharField(max_length=100)
    
class Comment(PostParent):
    username = models.ForeignKey('auth.User', related_name="user_comments")
    parent_post = models.ForeignKey('Post',related_name="post_comments")
    parent_comment = models.ForeignKey('Comment',related_name="reply_comments",blank=True,null=True)
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.text