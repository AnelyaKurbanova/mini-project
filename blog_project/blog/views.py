from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q 

def post_list(request):
    query = request.GET.get('q', '')  
    post_list = Post.objects.all()

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(post_list, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(request, 'blog/post_details.html', {'post': post, 'comments': comments})


@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content, author=request.user)
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html')


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return redirect('post_list', pk=post.pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, content=content, author=request.user)
        return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=post.pk)
