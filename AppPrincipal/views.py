from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, ProfileForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'AppPrincipal/post_list.html', {'posts': posts})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor, inicia sesión.')
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            messages.success(request, 'Post creado exitosamente.')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'AppPrincipal/create_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'AppPrincipal/post_detail.html', {'post': post})


def page_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'AppPrincipal/page_detail.html', {'post': post})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:  
        messages.error(request, 'No tienes permisos para editar este post.')
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post actualizado exitosamente.')
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'AppPrincipal/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:  
        messages.error(request, 'No tienes permisos para eliminar este post.')
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post eliminado exitosamente.')
        return redirect('post_list')
    return render(request, 'AppPrincipal/delete_post.html', {'post': post})


def about(request):
    return render(request, 'AppPrincipal/about.html')


@login_required
def view_profile(request):
    try:
        profile = request.user.profile
    except AttributeError:
        profile = None  
    return render(request, 'AppPrincipal/profile.html', {'user': request.user, 'profile': profile})

@login_required
def edit_profile(request):
    try:
        if request.method == 'POST':
            user_form = UserChangeForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('view_profile')
        else:
            user_form = UserChangeForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
    except AttributeError:
        return redirect('profile_error')  
    return render(request, 'AppPrincipal/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})