from django.shortcuts import render, redirect, get_object_or_404
from .form import BlogPostForm
from django.http import HttpResponse
from .models import BlogPost
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    query = request.GET.get('q', '')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        posts = BlogPost.objects.all()

    posts = posts.order_by('-updated_at')

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'query': query
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')  # Redirect to login if not authenticated
def blog_post_list(request):
    query = request.GET.get('q', '')

    if query:
        posts = BlogPost.objects.filter(
            Q(author=request.user) & (Q(title__icontains=query) | Q(content__icontains=query))
        )
    else:
        posts = BlogPost.objects.filter(author=request.user)

    posts = posts.order_by('-updated_at')

    paginator = Paginator(posts, 8)  # 8 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'query': query
    }
    return render(request, 'blog_list.html', context)


def blog_post_create(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login to create post.")
        return redirect('login')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, "Post created successfully!")
            return redirect('BlogPostList')
        else:
            messages.error(request, 'There were errors in your form submission.')
    else:
        form = BlogPostForm()

    return render(request, 'blog_create.html', {'form': form})


@login_required(login_url='login')
def blog_post_detail(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return HttpResponse("Blog post not found.", status=404)
    
    context = {'post': post}
    return render(request, 'blog_details.html', context)



@login_required(login_url='login')
def blog_post_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user  # Re-assign author to current user (optional if unchanged)
            updated_post.save()
            return redirect('BlogPostList')  # Make sure this URL name is defined in urls.py
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog_update.html', context)



@login_required(login_url='login')
def blog_post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('BlogPostList')
    return redirect('BlogPostDetail', pk=pk)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('BlogPostList')
        else:
            return HttpResponse("Invalid credentials", status=401)
    return render(request, 'login.html')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists", status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Authenticate and login the user automatically
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # ✅ Auto-login
            return redirect('Home')  # 🔁 Redirect to homepage or dashboard

    return render(request, 'signup.html')



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('Home')  # Redirect to home or login page after logout