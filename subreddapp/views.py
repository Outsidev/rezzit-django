from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.db.models import Count
from .models import Post,Comment
from .forms import CommentForm

# Create your views here.
def main_page(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('published_date')   
    return render(request, 'sub/main_page.html', {'posts':posts})

def main_page_news(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('-published_date')   
    return render(request, 'sub/main_page.html', {'posts':posts})

def main_page_tops(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('-points')   
    return render(request, 'sub/main_page.html', {'posts':posts})

def main_page_hots(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('-comment_counts')   
    return render(request, 'sub/main_page.html', {'posts':posts})



def comments_page(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments.all()
    return render(request, 'sub/comments_page.html', {'post':post,'comments':comments})

def send_comment(request):
    #not works for now
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=false)
            comm.username = "burk"
            comm.published_date = timezone.now()
            comm.save() 
    else:
        form = CommentForm()
    
    return HttpResponseRedirect('/')