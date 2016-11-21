from django.contrib import admin
from .models import Post_Main,Post_Comment

# Register your models here.
admin.site.register(Post_Main)
admin.site.register(Post_Comment)
