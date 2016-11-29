from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse,JsonResponse,Http404
from django.forms.models import model_to_dict
from django.template import TemplateDoesNotExist

from .models import Post,Comment
from .forms import CommentForm

# Create your views here.
def main_page(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('published_date')   
    return render(request, 'sub/main_page.html', {'posts':posts})

def main_page_news(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('-published_date')   
    return render(request, 'sub/main_page.html', {'posts':posts, 'basehtml':'sub/base_ajax.html'})

def main_page_tops(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('-points')   
    return render(request, 'sub/main_page.html', {'posts':posts, 'basehtml':'sub/base_ajax.html'})

def main_page_hots(request):
    posts = Post.objects.annotate(comment_counts = Count('post_comments')).order_by('-comment_counts')   
    return render(request, 'sub/main_page.html', {'posts':posts, 'basehtml':'sub/base_ajax.html'})


def get_template(request, template_name):
    try:
        return render(request, 'sub/kids/'+template_name+'.html')
    except TemplateDoesNotExist:
        return Http404


def comments_page(request, pk, slug):
    post = get_object_or_404(Post, pk=pk)
    comment_count = post.post_comments.count()
    comments = post.post_comments.prefetch_related('reply_comments').filter(parent_comment__isnull=True).order_by('-published_date')
    return render(request, 'sub/comments_page.html', {'post':post,'comments':comments, 'comment_count':comment_count})

def make_comment(request):    
    if request.method == 'POST':
        text = request.POST.get('text')
        parentpost_id = int(request.POST.get('parentpost_id'))
        parent_comment = None
        try:
            parentcomment_id = int(request.POST.get('parentcomment_id'))
            parent_comment = Comment.objects.get(pk = parentcomment_id)
        except Exception:
            parent_comment = None          

        comm = Comment(text = text, parent_post = Post.objects.get(pk = parentpost_id), 
                                    parent_comment = parent_comment,
                                    username= request.user, published_date = timezone.now())
        comm.save()
        return render(request, 'sub/comment_box.html',{'comment':comm})

    return HttpResponse("nope_no_return")

def give_point(request):
    if request.method == 'GET':
        obj_id = request.GET['post_id']
        arrow_dir = request.GET['arrow_dir']
        what_type = request.GET['what_type']
        obj = None

        if what_type == "post":
            obj = Post.objects.get(pk=int(obj_id))
        elif what_type == "comment":                
            obj = Comment.objects.get(pk=int(obj_id))
        
        if obj != None:            
            if arrow_dir == "true":        
                obj.point_up()
            else:
                obj.point_down()

    return HttpResponse(obj.points)