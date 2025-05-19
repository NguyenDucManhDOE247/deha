from itertools import chain
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q, Prefetch, Count
from django.core.paginator import Paginator
import logging
from django.contrib import messages
from . models import Followers, LikePost, Post, Profile, Comment
from .forms import SignUpForm, LoginForm, PostForm, ProfileForm, CommentForm
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                
                my_user = User.objects.create_user(username, email, password)
                my_user.save()
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                
                auth_login(request, my_user)
                messages.success(request, "Account registration successful!")
                return redirect('/')
            except IntegrityError as e:
                logger.error(f"IntegrityError in signup: {e}")
                messages.error(request, "User already exists")
            except Exception as e:
                logger.error(f"Error in signup: {e}")
                messages.error(request, "An error occurred, please try again")
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('/')
                
                messages.error(request, "Invalid login credentials")
            except Exception as e:
                logger.error(f"Error in login: {e}")
                messages.error(request, "An error occurred, please try again")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('/login')


@login_required(login_url='/login')
def home(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, id_user=request.user.id)
        profile.save()
    
    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)
    
    post = Post.objects.filter(
        Q(user=request.user.username) | Q(user__in=following_users)
    ).order_by('-created_at')
    
    all_profiles = Profile.objects.select_related('user').all()
    
    username_profile_map = {}
    for prof in all_profiles:
        username_profile_map[prof.user.username] = prof
    
    paginator = Paginator(post, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post': page_obj,
        'profile': profile,
        'page_obj': page_obj,
        'all_profiles': all_profiles,
        'username_profile_map': username_profile_map,
        'user': request.user.username,
    }
    return render(request, 'main.html', context)
    

@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.user = request.user.username
                post.save()
                
                messages.success(request, "Post created successfully!")
                return redirect('/')
            except Exception as e:
                logger.error(f"Error in upload: {e}")
                messages.error(request, "An error occurred when creating the post")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return redirect('/')

@login_required(login_url='/login')
def likes(request, id):
    if request.method == 'GET':
        try:
            username = request.user.username
            post = get_object_or_404(Post, id=id)

            like_filter = LikePost.objects.filter(post_id=id, username=username).first()

            if like_filter is None:
                new_like = LikePost.objects.create(post_id=id, username=username)
                post.no_of_likes = post.no_of_likes + 1
                messages.info(request, "Post liked")
            else:
                like_filter.delete()
                post.no_of_likes = max(0, post.no_of_likes - 1)
                messages.info(request, "Post unliked")

            post.save()

            return redirect('/#'+str(id))
        except Exception as e:
            logger.error(f"Error in likes: {e}")
            messages.error(request, "An error occurred during this operation")
            return redirect('/')
    
@login_required(login_url='/login')
def explore(request):
    try:
        posts = Post.objects.all().order_by('-created_at')
        
        post_data = []
        for post in posts:
            try:
                post_owner = User.objects.get(username=post.user)
                post_profile = Profile.objects.get(user=post_owner)
                post.user_profile = post_profile
            except (User.DoesNotExist, Profile.DoesNotExist):
                pass
            post_data.append(post)
            
        paginator = Paginator(post_data, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()

        context = {
            'post': page_obj,
            'profile': profile,
            'page_obj': page_obj,
        }
        return render(request, 'explore.html', context)
    except Exception as e:
        logger.error(f"Error in explore: {e}")
        messages.error(request, "An error occurred while loading the explore page")
        return redirect('/')
    
@login_required(login_url='/login')
def profile(request, id_user):
    try:
        user_object = User.objects.get(username=id_user)
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()
        
        try:
            user_profile = Profile.objects.get(user=user_object)
        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(user=user_object, id_user=user_object.id)
            user_profile.save()
        
        user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
        paginator = Paginator(user_posts, 9)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        user_post_length = user_posts.count() 

        follower = request.user.username
        user = id_user
        
        if Followers.objects.filter(follower=follower, user=user).exists():
            follow_unfollow = 'Unfollow'
        else:
            follow_unfollow = 'Follow'

        user_followers = Followers.objects.filter(user=id_user).count()
        user_following = Followers.objects.filter(follower=id_user).count()

        context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': page_obj, 
            'user_post_length': user_post_length,
            'profile': profile,
            'follow_unfollow': follow_unfollow,
            'user_followers': user_followers,
            'user_following': user_following,
            'page_obj': page_obj,
        }
        
        if request.user.username == id_user:
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, instance=user_profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Profile updated successfully!")
                    return redirect('/profile/'+id_user)
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{error}")
            else:
                form = ProfileForm(instance=user_profile)
                context['form'] = form
                
        return render(request, 'profile.html', context)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/')
    except Exception as e:
        logger.error(f"Error in profile view: {e}")
        messages.error(request, "An error occurred while loading profile")
        return redirect('/')

@login_required(login_url='/login')
def delete(request, id):
    try:
        post = Post.objects.get(id=id)
        if post.user == request.user.username:
            post.delete()
            messages.success(request, "Post deleted successfully!")
        else:
            messages.error(request, "You don't have permission to delete this post")
        return redirect('/profile/'+ request.user.username)
    except Post.DoesNotExist:
        messages.error(request, "Post not found")
        return redirect('/profile/'+ request.user.username)
    except Exception as e:
        logger.error(f"Error in delete: {e}")
        messages.error(request, "An error occurred while deleting the post")
        return redirect('/profile/'+ request.user.username)


@login_required(login_url='/login')
def search_results(request):
    try:
        query = request.GET.get('q', '')
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()

        users = Profile.objects.filter(user__username__icontains=query).select_related('user')
        
        posts_queryset = Post.objects.filter(caption__icontains=query)
        posts = []
        for post in posts_queryset:
            try:
                post_owner = User.objects.get(username=post.user)
                post_profile = Profile.objects.get(user=post_owner)
                post.user_profile = post_profile
            except (User.DoesNotExist, Profile.DoesNotExist):
                pass
            posts.append(post)
        
        posts_paginator = Paginator(posts, 6)
        posts_page = request.GET.get('posts_page')
        posts_page_obj = posts_paginator.get_page(posts_page)
        
        users_paginator = Paginator(users, 10)
        users_page = request.GET.get('users_page')
        users_page_obj = users_paginator.get_page(users_page)

        context = {
            'query': query,
            'users': users_page_obj,
            'posts': posts_page_obj,
            'profile': profile,
            'users_page_obj': users_page_obj,
            'posts_page_obj': posts_page_obj,
        }
        return render(request, 'search_user.html', context)
    except Exception as e:
        logger.error(f"Error in search_results: {e}")
        messages.error(request, "An error occurred during search")
        return redirect('/')

@login_required(login_url='/login')
def home_post(request, id):
    try:
        post = get_object_or_404(Post, id=id)
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()
        
        try:
            post_owner = User.objects.get(username=post.user)
            post_owner_profile = Profile.objects.get(user=post_owner)
            post.user_profile = post_owner_profile  
        except (User.DoesNotExist, Profile.DoesNotExist):
            post_owner_profile = None
        
        comments = Comment.objects.filter(post=post).select_related('post')
        
        comment_form = CommentForm()
        
        all_profiles = Profile.objects.select_related('user').all()
        
        username_profile_map = {}
        for prof in all_profiles:
            username_profile_map[prof.user.username] = prof
            
        context = {
            'post': [post],  
            'profile': profile,
            'post_owner_profile': post_owner_profile,
            'all_profiles': all_profiles,
            'username_profile_map': username_profile_map,
            'single_post_view': True,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, 'main.html', context)
    except Post.DoesNotExist:
        messages.error(request, "Post not found")
        return redirect('/')
    except Exception as e:
        logger.error(f"Error in home_post: {e}")
        messages.error(request, "An error occurred while loading the post")
        return redirect('/')


@login_required(login_url='/login')
def follow(request):
    if request.method == 'POST':
        try:
            follower = request.POST['follower']
            user = request.POST['user']

            if follower == user:
                messages.error(request, "You cannot follow yourself")
                return redirect('/profile/'+user)

            existing_follow, created = Followers.objects.get_or_create(follower=follower, user=user)
            if not created:
                existing_follow.delete()
                messages.info(request, f"Unfollowed @{user}")
            else:
                messages.success(request, f"Now following @{user}")

            return redirect('/profile/'+user)
        except KeyError:
            logger.error("Missing follower or user in POST data")
            messages.error(request, "Invalid data")
            return redirect('/')
        except Exception as e:
            logger.error(f"Error in follow: {e}")
            messages.error(request, "An error occurred while following")
            return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/login')
@require_POST
def add_comment(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user.username
            comment.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'comment_id': str(comment.id),
                    'user': comment.user,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%b %d, %Y, %I:%M %p')
                })
            
            messages.success(request, "Comment added successfully!")
            return redirect(f'/post/{post_id}')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            
            messages.error(request, "Error adding comment.")
            return redirect(f'/post/{post_id}')
    except Exception as e:
        logger.error(f"Error in add_comment: {e}")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        messages.error(request, "An error occurred while adding your comment")
        return redirect(f'/post/{post_id}')

@login_required(login_url='/login')
def delete_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        if comment.user == request.user.username or comment.post.user == request.user.username:
            post_id = comment.post.id
            comment.delete()
            messages.success(request, "Comment deleted successfully")
            return redirect(f'/post/{post_id}')
        else:
            messages.error(request, "You don't have permission to delete this comment")
            return redirect('/')
    except Exception as e:
        logger.error(f"Error in delete_comment: {e}")
        messages.error(request, "An error occurred while deleting the comment")
        return redirect('/')