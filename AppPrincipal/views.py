from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post

def post_list(request):
    posts = Post.objects.all() 
    return render(request, 'AppPrincipal/post_list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('post_list')  
    else:
        form = PostForm()
    return render(request, 'AppPrincipal/create_post.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'AppPrincipal/edit_post.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'AppPrincipal/delete_post.html', {'post': post})