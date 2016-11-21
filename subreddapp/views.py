from django.shortcuts import render
from django.utils import timezone
from .models import Post_Main

# Create your views here.
def main_page(request):
    posts = Post_Main.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'sub/main_page.html', {'posts':posts})

def post_comments(request):
    return render(request, 'sub/post_comments.html', {})
