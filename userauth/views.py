from itertools import chain
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
import logging
from . models import Followers, LikePost, Post, Profile

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        try:
            fnm = request.POST.get('fnm')
            emailid = request.POST.get('emailid')
            pwd = request.POST.get('pwd')
            
            if User.objects.filter(username=fnm).exists():
                invalid = "Tên người dùng đã tồn tại"
                return render(request, 'signup.html', {'invalid': invalid})
            
            if User.objects.filter(email=emailid).exists():
                invalid = "Email đã được sử dụng"
                return render(request, 'signup.html', {'invalid': invalid})
            
            my_user = User.objects.create_user(fnm, emailid, pwd)
            my_user.save()
            
            user_model = User.objects.get(username=fnm)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            
            auth_login(request, my_user)
            return redirect('/')
            
        except IntegrityError as e:
            logger.error(f"IntegrityError in signup: {e}")
            invalid = "Người dùng đã tồn tại"
            return render(request, 'signup.html', {'invalid': invalid})
        except Exception as e:
            logger.error(f"Error in signup: {e}")
            invalid = "Có lỗi xảy ra, vui lòng thử lại"
            return render(request, 'signup.html', {'invalid': invalid})
    
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        try:
            fnm = request.POST.get('fnm')
            pwd = request.POST.get('pwd')
            
            userr = authenticate(request, username=fnm, password=pwd)
            if userr is not None:
                auth_login(request, userr)
                return redirect('/')
            
            invalid = "Thông tin đăng nhập không chính xác"
            return render(request, 'login.html', {'invalid': invalid})
        except Exception as e:
            logger.error(f"Error in login: {e}")
            invalid = "Có lỗi xảy ra, vui lòng thử lại"
            return render(request, 'login.html', {'invalid': invalid})
    
    return render(request, 'login.html')

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def home(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, id_user=request.user.id)
        profile.save()
    
    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)
    post = Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')

    context = {
        'post': post,
        'profile': profile,
    }
    return render(request, 'main.html', context)
    

@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        try:
            user = request.user.username
            image = request.FILES.get('image_upload')
            caption = request.POST['caption']
            
            if not image:
                return redirect('/')
            
            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()
            
            return redirect('/')
        except Exception as e:
            logger.error(f"Error in upload: {e}")
            return redirect('/')
    else:
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
            else:
                like_filter.delete()
                post.no_of_likes = max(0, post.no_of_likes - 1)

            post.save()

            return redirect('/#'+str(id))
        except Exception as e:
            logger.error(f"Error in likes: {e}")
            return redirect('/')
    
@login_required(login_url='/login')
def explore(request):
    try:
        post = Post.objects.all().order_by('-created_at')
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()

        context = {
            'post': post,
            'profile': profile
        }
        return render(request, 'explore.html', context)
    except Exception as e:
        logger.error(f"Error in explore: {e}")
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
        user_post_length = len(user_posts)

        follower = request.user.username
        user = id_user
        
        if Followers.objects.filter(follower=follower, user=user).first():
            follow_unfollow = 'Unfollow'
        else:
            follow_unfollow = 'Follow'

        user_followers = len(Followers.objects.filter(user=id_user))
        user_following = len(Followers.objects.filter(follower=id_user))

        context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'profile': profile,
            'follow_unfollow': follow_unfollow,
            'user_followers': user_followers,
            'user_following': user_following,
        }
        
        if request.user.username == id_user:
            if request.method == 'POST':
                try:
                    if request.FILES.get('image') is None:
                        image = user_profile.profileimg
                        bio = request.POST['bio']
                        location = request.POST['location']

                        user_profile.profileimg = image
                        user_profile.bio = bio
                        user_profile.location = location
                        user_profile.save()
                    else:
                        image = request.FILES.get('image')
                        bio = request.POST['bio']
                        location = request.POST['location']

                        user_profile.profileimg = image
                        user_profile.bio = bio
                        user_profile.location = location
                        user_profile.save()
                    
                    return redirect('/profile/'+id_user)
                except Exception as e:
                    logger.error(f"Error updating profile: {e}")
                    return redirect('/profile/'+id_user)
                
        return render(request, 'profile.html', context)
    except User.DoesNotExist:
        return redirect('/')
    except Exception as e:
        logger.error(f"Error in profile view: {e}")
        return redirect('/')

@login_required(login_url='/login')
def delete(request, id):
    try:
        post = Post.objects.get(id=id)
        if post.user == request.user.username:
            post.delete()
        return redirect('/profile/'+ request.user.username)
    except Post.DoesNotExist:
        return redirect('/profile/'+ request.user.username)
    except Exception as e:
        logger.error(f"Error in delete: {e}")
        return redirect('/profile/'+ request.user.username)


@login_required(login_url='/login')
def search_results(request):
    try:
        query = request.GET.get('q', '')
        
        try:
            profile = Profile.objects.filter(user=request.user).first()
            if not profile:
                profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                profile.save()
        except Exception as e:
            logger.error(f"Error creating profile in search: {e}")
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()

        users = Profile.objects.filter(user__username__icontains=query)
        posts = Post.objects.filter(caption__icontains=query)

        context = {
            'query': query,
            'users': users,
            'posts': posts,
            'profile': profile
        }
        return render(request, 'search_user.html', context)
    except Exception as e:
        logger.error(f"Error in search_results: {e}")
        return redirect('/')

@login_required(login_url='/login')
def home_post(request, id):
    try:
        post = Post.objects.get(id=id)
        profile = Profile.objects.get(user=request.user)
        context = {
            'post': post,
            'profile': profile
        }
        return render(request, 'main.html', context)
    except Post.DoesNotExist:
        return redirect('/')
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, id_user=request.user.id)
        profile.save()
        return redirect('/')
    except Exception as e:
        logger.error(f"Error in home_post: {e}")
        return redirect('/')


@login_required(login_url='/login')
def follow(request):
    if request.method == 'POST':
        try:
            follower = request.POST['follower']
            user = request.POST['user']

            if follower == user:
                return redirect('/profile/'+user)

            existing_follow = Followers.objects.filter(follower=follower, user=user).first()
            if existing_follow:
                existing_follow.delete()
            else:
                new_follower = Followers.objects.create(follower=follower, user=user)
                new_follower.save()

            return redirect('/profile/'+user)
        except KeyError:
            logger.error("Missing follower or user in POST data")
            return redirect('/')
        except Exception as e:
            logger.error(f"Error in follow: {e}")
            return redirect('/')
    else:
        return redirect('/')