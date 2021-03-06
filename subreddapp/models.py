from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class PostParent(models.Model):
    text = models.TextField(default="")
    published_date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)

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


    def __unicode__(self):
        return self.title

class Post(PostParent):
    user = models.ForeignKey(User, related_name="user_mainposts")
    link_adress = models.CharField(max_length=200)
    title =  models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)

    def save_it(self):
        self.published_date = timezone.now()
        self.slug = slugify(self.title)
        self.save() 
    
class Comment(PostParent):
    user = models.ForeignKey(User, related_name="user_comments")
    parent_post = models.ForeignKey('Post',related_name="post_comments")
    parent_comment = models.ForeignKey('Comment',related_name="reply_comments",blank=True,null=True)

    def __unicode__(self):
        return self.text

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    register_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.user.username;