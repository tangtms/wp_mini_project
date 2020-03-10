from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

from management.models import Post, Comment

@login_required
def post_add(request):
    post = Post.objects.all()
    current_user = request.user
    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            user_id=current_user,
            status=True
        )
    else:
        post = Post.objects.none()

    context = {
        'post': post,
    }
    return render(request, template_name='post_form.html', context=context)

@login_required
@permission_required('management.change_post')
def post_update(request, post_id):
    post = Post.objects.get(pk=post_id)
    current_user = request.user
    if current_user == post.user_id: #backend check if post user = edit user
        if request.method == 'POST':
            post.title = request.POST.get('title')
            post.content = request.POST.get('content')
            post.save()

        context = {
            'post': post,
        }
        return render(request, template_name='post_form.html', context=context)
    return HttpResponseForbidden()

@permission_required('management.change_post')
@login_required
def post_list(request):
    post = Post.objects.all()

    return render(request, template_name='post_list.html', context={
        'post': post
    })

@login_required
def comment_delete(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    cur_post = comment.post_id.id

    comment.delete()

    return redirect('post_detail', post_id=cur_post)

def comment_edit(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    cur_post = comment.post_id.id
    if request.method == 'POST':
        comment.content=request.POST.get('content')
        comment.save()
        return redirect('post_detail', post_id=cur_post)
    
    context = {
            'comment': comment,
        }
    return render(request, template_name='comment_edit.html', context=context)



@login_required
def post_hide(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = False
    post.save()

    return redirect('post_list')

@login_required
def post_show(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = True
    post.save()

    return redirect('post_list')


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
    comment_cnt = len(comment)
    return render(request, template_name='detail.html', context={
        'post': post,
        'comment': comment,
        'comment_cnt': comment_cnt
    })