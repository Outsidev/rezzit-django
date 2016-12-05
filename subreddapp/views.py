from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse,JsonResponse,Http404
from django.forms.models import model_to_dict
from django.template import TemplateDoesNotExist
from django.contrib.auth import authenticate,login,logout

from .models import Post,Comment
from .forms import CommentForm,UserForm,UserProfileForm,PostForm

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

def comments_page(request, pk, slug):
    post = get_object_or_404(Post, pk=pk)
    comment_count = post.post_comments.count()
    comments = post.post_comments.prefetch_related('reply_comments').filter(parent_comment__isnull=True).order_by('-published_date')
    return render(request, 'sub/comments_page.html', {'post':post,'comments':comments, 'comment_count':comment_count})

def make_post_page(request):
    return render(request, 'sub/make_post_page.html')

def login_view(request):
    logged=False;
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("yep1")
            login(request, user)
            logged=True
            
    return HttpResponse(logged)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse("logout.")
    else:
        return Http404

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        print(request.POST);
        print(user_form.is_valid());
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password) #hashing
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            registered = True
            login(request,user)
            
    return HttpResponse(registered)

def get_template(request, template_name):
    try:
        return render(request, 'sub/kids/'+template_name+'.html')
    except TemplateDoesNotExist:
        return Http404

def make_post(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save_it()
            return redirect('comments_page', pk=post.pk, slug=post.slug)

    return render(request, 'sub/make_post_page.html')

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
                                    user= request.user, published_date = timezone.now())
        comm.save()
        return render(request, 'sub/comment_box.html',{'comment':comm})

    return Http404

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