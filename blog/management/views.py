from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from management.models import Post, Comment
# Create your views here.
@login_required
def post_add(request):
    post = Post.objects.all()
    current_user = request.user
    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            user_id=current_user
        )
    else:
        post = Post.objects.none()

    context = {
        'post': post,
    }
    return render(request, template_name='post_form.html', context=context)

@login_required
def post_update(request):
    post = Post.objects.all()

    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
        )
    else:
        post = Post.objects.none()

    context = {
        'post': post,
    }
    return render(request, template_name='post_form.html', context=context)

@login_required
def post_list(request):
    post = Post.objects.all()

    return render(request, template_name='post_list.html', context={
        'post': post
    })

def detail(request, post_id):
    current_user = request.user
    if request.method == 'POST':
        Comment.objects.create(
            content=request.POST.get('content'),
            user_id=current_user,
            post_id=Post.objects.get(pk=post_id)
        )
    
    post = Post.objects.get(pk=post_id)
    comment = Comment.objects.filter(post_id=post_id)
    return render(request, template_name='detail.html', context={
        'post': post,
        'comment': comment
    })