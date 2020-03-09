from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from management.models import Post, Comment

#login, logout, register, index

def my_login(request):
    context = {} 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user: 
            login(request, user)

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='login.html', context=context)

def my_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_chk = request.POST.get('password_chk')

        if User.objects.filter(username=username).exists(): #if user already exists
            context['username'] = username
            context['error'] = 'Username already exists'
        elif password != password_chk: #if password not match
            context['username'] = username
            context['error'] = 'Password not match'
        else:
            user = User.objects.create_user(username, '', password)
            user_group = Group.objects.get(name='User') #auto add new user to group User
            user_group.user_set.add(user)
            return redirect('login')

    return render(request, template_name='register.html', context=context)

def index(request):
    search_txt = request.GET.get('inputSearch', '')
    print(search_txt)

    post = Post.objects.filter(
        title__icontains=search_txt,
        status=1 #is publish
    )

    return render(request, template_name='index.html', context={
        'search_txt': search_txt,
        'post': post
    })