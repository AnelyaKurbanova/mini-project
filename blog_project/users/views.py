from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Follow
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile', pk=user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile.bio = bio
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile', pk=request.user.pk)
    return render(request, 'users/edit_profile.html', {'profile': profile})


@login_required
def follow_user(request, pk):
    user_to_follow = get_object_or_404(User, pk=pk)
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', pk=pk)


@login_required
def unfollow_user(request, pk):
    user_to_unfollow = get_object_or_404(User, pk=pk)
    follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    follow.delete()
    return redirect('profile', pk=pk)
