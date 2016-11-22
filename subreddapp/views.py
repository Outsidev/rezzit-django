from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post_Main,Post_Comment

# Create your views here.
def main_page(request):
    posts = Post_Main.objects.all().order_by('-published_date')
    return render(request, 'sub/main_page.html', {'posts':posts})

def post_comments(request, pk):
    post = get_object_or_404(Post_Main, pk=pk)
    comments = post.post_comments.all()
    return render(request, 'sub/post_comments.html', {'post':post,'comments':comments})
