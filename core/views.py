from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm,PostForm,CommentForm,ReplyForm
from django.contrib.auth import authenticate , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Post, Topic , Like_Dislike ,Comment
from django.db.models import Q
from django.contrib import messages
def home(request):
    topic_id = request.GET.get('topic_id')
    query = request.GET.get('search')
    posts = Post.objects.all()
    
    if topic_id :
        posts = posts.filter(topic_id = topic_id)

    if query :
        posts = posts.filter(Q(title__icontains = query) | Q(text__icontains = query))
    
    topics = Topic.objects.all()
    context = {'posts':posts,'topics':topics}
    return render(request,"core/index.html",context)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    context={"form":form}
    return render(request,"core/register.html",context)

def login_page(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post-list')  # Redirect to the post list after successful login
        else:
            messages.error(request, "Invalid username or password")
            print("Login failed for:", username)

    context={}
    return render(request,"core/login.html",context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def post_form(request):
    if request.method=="POST":
        print(request.user)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user=request.user
            if not post.topic:
                messages.error(request, "Please select a topic.")
                return redirect("post-form")
            post.save()
            return redirect("post-list")
    
        else:
            print(form.errors)
    else:
        form=PostForm()
    context={"form":form}
    return render(request,"core/postform.html",context)

def post_detail(request,pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.all()
    if request.method== "POST":

        if "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect (request.path)
            
        elif "reply_submit" in request.POST:
            print(request.POST)
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.user = request.user
                reply.comment = get_object_or_404(Comment,id=request.POST.get('comment_id'))
                reply.save()
                return redirect(f"{request.path}?comment_id={reply.comment.id}")
    else:
        comment_form = CommentForm()
        reply_form = ReplyForm()
    context={'post':post,'comment_form':comment_form,'reply_form':reply_form,'comments':comments}
    return render(request,"core/post_detail.html",context)

def like_dislike_post(request,pk,vote_type):
    post = get_object_or_404(Post,id=pk)
    like_dislike,created = Like_Dislike.objects.get_or_create(user=request.user,post=post)

    if like_dislike.vote_type == vote_type:
        like_dislike.delete()
    else:
        like_dislike.vote_type = vote_type
        like_dislike.save()
    
    return redirect('post-detail',pk=post.id)

def save_post(request,post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if post in user.saved_posts.all() :
        user.saved_posts.remove(post)
    else:
        user.saved_posts.add(post)
    
    return redirect('post-list')

def saved_posts_list(request):
    user = request.user
    saved_posts = user.saved_posts.all()
    return render(request,"core/saved_posts.html",context={"saved_posts":saved_posts})