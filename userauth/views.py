from itertools import chain
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.db.models import Q, Prefetch, Count
from django.core.paginator import Paginator
import logging
from django.contrib import messages
from . models import Followers, LikePost, Post, Profile, Comment, Tag, Bookmark
from .forms import SignUpForm, LoginForm, PostForm, ProfileForm, CommentForm
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'
    
    def form_valid(self, form):
        try:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            
            auth_login(self.request, my_user)
            messages.success(self.request, "Account registration successful!")
            return super().form_valid(form)
        except IntegrityError as e:
            logger.error(f"IntegrityError in signup: {e}")
            messages.error(self.request, "User already exists")
            return self.form_invalid(form)
        except Exception as e:
            logger.error(f"Error in signup: {e}")
            messages.error(self.request, "An error occurred, please try again")
            return self.form_invalid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    
    def form_valid(self, form):
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                auth_login(self.request, user)
                messages.success(self.request, "Login successful!")
                return super().form_valid(form)
            
            messages.error(self.request, "Invalid login credentials")
            return self.form_invalid(form)
        except Exception as e:
            logger.error(f"Error in login: {e}")
            messages.error(self.request, "An error occurred, please try again")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successful!")
        return redirect('/login')


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'post'
    paginate_by = 10
    login_url = '/login'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                self.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                self.profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                self.profile.save()
        else:
            self.profile = None
    
    def get_queryset(self):
        following_users = Followers.objects.filter(follower=self.request.user.username).values_list('user', flat=True)
        
        queryset = Post.objects.filter(
            Q(user=self.request.user.username) | Q(user__in=following_users)
        ).prefetch_related('comments', 'tags').order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_bookmarks = Bookmark.objects.filter(user=self.request.user.username).values_list('post_id', flat=True)
        user_likes = LikePost.objects.filter(username=self.request.user.username).values_list('post_id', flat=True)
        
        all_profiles = Profile.objects.select_related('user').all()
        
        username_profile_map = {}
        for prof in all_profiles:
            username_profile_map[prof.user.username] = prof
        
        tag_list = Tag.objects.all().order_by('name')
        
        context.update({
            'profile': self.profile,
            'all_profiles': all_profiles,
            'username_profile_map': username_profile_map,
            'user': self.request.user.username,
            'tag_list': tag_list,
            'user_bookmarks': user_bookmarks,
            'user_likes': user_likes,
        })
        return context


class UploadPostView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.user = request.user.username
                post.save()
                
                form.save_m2m()
                
                messages.success(request, "Post created successfully!")
            except Exception as e:
                logger.error(f"Error in upload: {e}")
                messages.error(request, "An error occurred when creating the post")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
        return redirect('/')


class LikePostView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request, id):
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

            referer = request.META.get('HTTP_REFERER', '')
            if '/tag/' in referer:
                tag_name = referer.split('/tag/')[1].split('/')[0]
                return redirect(f'/tag/{tag_name}/')
            elif '/post/' in referer:
                return redirect(f'/post/{id}')
            elif '/bookmarks/' in referer:
                return redirect(f'/bookmarks/#{id}')
            else:
                return redirect('/#'+str(id))
        except Exception as e:
            logger.error(f"Error in likes: {e}")
            messages.error(request, "An error occurred during this operation")
            return redirect('/')


class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    context_object_name = 'post'
    paginate_by = 12
    login_url = '/login'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                self.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                self.profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                self.profile.save()
        else:
            self.profile = None
    
    def get_queryset(self):
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
        return post_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_object'
    slug_field = 'username'
    slug_url_kwarg = 'id_user'
    login_url = '/login'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                self.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                self.profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                self.profile.save()
        else:
            self.profile = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = self.get_object()
        
        try:
            user_profile = Profile.objects.get(user=user_object)
        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(user=user_object, id_user=user_object.id)
            user_profile.save()
        
        user_posts = Post.objects.filter(user=user_object.username).order_by('-created_at')
        paginator = Paginator(user_posts, 9)  
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        user_post_length = user_posts.count() 

        follower = self.request.user.username
        user = user_object.username
        
        if Followers.objects.filter(follower=follower, user=user).exists():
            follow_unfollow = 'Unfollow'
        else:
            follow_unfollow = 'Follow'

        user_followers = Followers.objects.filter(user=user).count()
        user_following = Followers.objects.filter(follower=user).count()
        
        context.update({
            'user_profile': user_profile,
            'user_posts': page_obj,
            'user_post_length': user_post_length,
            'profile': self.profile,
            'follow_unfollow': follow_unfollow,
            'user_followers': user_followers,
            'user_following': user_following,
            'page_obj': page_obj,
        })
        
        if self.request.user.username == user_object.username:
            if self.request.method == 'POST':
                form = ProfileForm(self.request.POST, self.request.FILES, instance=user_profile)
                if form.is_valid():
                    form.save()
                    messages.success(self.request, "Profile updated successfully!")
                    return redirect('/profile/'+user_object.username)
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(self.request, f"{error}")
                context['form'] = form
            else:
                context['form'] = ProfileForm(instance=user_profile)
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class DeletePostView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request, id):
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


class SearchResultsView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request):
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


class SinglePostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'
    login_url = '/login'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                self.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                self.profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                self.profile.save()
        else:
            self.profile = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
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
        
        context.update({
            'post': [post],  
            'profile': self.profile,
            'post_owner_profile': post_owner_profile,
            'all_profiles': all_profiles,
            'username_profile_map': username_profile_map,
            'single_post_view': True,
            'comments': comments,
            'comment_form': comment_form
        })
        
        return context


class FollowView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def post(self, request):
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


class AddCommentView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def post(self, request, post_id):
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


class DeleteCommentView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request, comment_id):
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


class ManageTagsView(LoginRequiredMixin, View):
    login_url = '/login'
    template_name = 'manage_tags.html'
    
    def get(self, request):
        tags = Tag.objects.all().order_by('name')
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, id_user=request.user.id)
            profile.save()
        
        context = {
            'tags': tags,
            'profile': profile,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        tag_name = request.POST.get('tag_name', '').strip()
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name.lower())
            if created:
                messages.success(request, f"Tag '{tag_name}' created successfully!")
            else:
                messages.info(request, f"Tag '{tag_name}' already exists.")
        else:
            messages.error(request, "Tag name cannot be empty.")
        
        return self.get(request)


class TagPostsView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'tag_posts.html'
    context_object_name = 'tag'
    slug_field = 'name'
    slug_url_kwarg = 'tag_name'
    login_url = '/login'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                self.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                self.profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                self.profile.save()
        else:
            self.profile = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        
        posts = tag.posts.all().order_by('-created_at')
        
        user_bookmarks = Bookmark.objects.filter(user=self.request.user.username).values_list('post_id', flat=True)
        
        all_profiles = Profile.objects.select_related('user').all()
        
        username_profile_map = {}
        for prof in all_profiles:
            username_profile_map[prof.user.username] = prof
        
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        tag_list = Tag.objects.all().order_by('name')
        
        context.update({
            'post': page_obj,
            'profile': self.profile,
            'page_obj': page_obj,
            'all_profiles': all_profiles,
            'username_profile_map': username_profile_map,
            'user': self.request.user.username,
            'tag_list': tag_list,
            'user_bookmarks': user_bookmarks,
        })
        
        return context


class DeleteTagView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request, tag_id):
        try:
            tag = get_object_or_404(Tag, id=tag_id)
            
            tag_name = tag.name
            tag.delete()
            messages.success(request, f"Tag '{tag_name}' deleted successfully!")
            return redirect('/tags/')
        except Exception as e:
            logger.error(f"Error in delete_tag: {e}")
            messages.error(request, "An error occurred while deleting the tag")
            return redirect('/tags/')


class BookmarkView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request, id):
        try:
            username = request.user.username
            post = get_object_or_404(Post, id=id)

            bookmark_filter = Bookmark.objects.filter(post=post, user=username).first()

            if bookmark_filter is None:
                new_bookmark = Bookmark.objects.create(post=post, user=username)
                messages.success(request, "Post bookmarked successfully!")
            else:
                bookmark_filter.delete()
                messages.info(request, "Post removed from bookmarks")

            referer = request.META.get('HTTP_REFERER', '')
            if '/tag/' in referer:
                tag_name = referer.split('/tag/')[1].split('/')[0]
                return redirect(f'/tag/{tag_name}/')
            elif '/post/' in referer:
                return redirect(f'/post/{id}')
            elif '/bookmarks/' in referer:
                return redirect(f'/bookmarks/#{id}')
            else:
                return redirect('/#'+str(id))
                
        except Exception as e:
            logger.error(f"Error in bookmark: {e}")
            messages.error(request, "An error occurred during this operation")
            return redirect('/')


class BookmarksView(LoginRequiredMixin, ListView):
    template_name = 'bookmarks.html'
    context_object_name = 'post'
    paginate_by = 10
    login_url = '/login'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                self.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                self.profile = Profile.objects.create(user=request.user, id_user=request.user.id)
                self.profile.save()
        else:
            self.profile = None
    
    def get_queryset(self):
        user_bookmarks = Bookmark.objects.filter(user=self.request.user.username).order_by('-created_at')
        bookmarked_posts = [bookmark.post for bookmark in user_bookmarks]
        return bookmarked_posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_bookmarks = Bookmark.objects.filter(user=self.request.user.username).values_list('post_id', flat=True)
        user_likes = LikePost.objects.filter(username=self.request.user.username).values_list('post_id', flat=True)
        
        all_profiles = Profile.objects.select_related('user').all()
        
        username_profile_map = {}
        for prof in all_profiles:
            username_profile_map[prof.user.username] = prof
        
        context.update({
            'profile': self.profile,
            'all_profiles': all_profiles,
            'username_profile_map': username_profile_map,
            'user': self.request.user.username,
            'user_bookmarks': user_bookmarks,
            'user_likes': user_likes,
        })
        
        return context

def signup(request):
    return SignUpView.as_view()(request)

def login(request):
    return LoginView.as_view()(request)

@login_required(login_url='/login')
def logout_view(request):
    return LogoutView.as_view()(request)

@login_required(login_url='/login')
def home(request):
    return HomeView.as_view()(request)

@login_required(login_url='/login')
def upload(request):
    return UploadPostView.as_view()(request)

@login_required(login_url='/login')
def likes(request, id):
    return LikePostView.as_view()(request, id=id)

@login_required(login_url='/login')
def explore(request):
    return ExploreView.as_view()(request)

@login_required(login_url='/login')
def profile(request, id_user):
    return ProfileView.as_view()(request, id_user=id_user)

@login_required(login_url='/login')
def delete(request, id):
    return DeletePostView.as_view()(request, id=id)

@login_required(login_url='/login')
def search_results(request):
    return SearchResultsView.as_view()(request)

@login_required(login_url='/login')
def home_post(request, id):
    return SinglePostView.as_view()(request, id=id)

@login_required(login_url='/login')
def follow(request):
    return FollowView.as_view()(request)

@login_required(login_url='/login')
@require_POST
def add_comment(request, post_id):
    return AddCommentView.as_view()(request, post_id=post_id)

@login_required(login_url='/login')
def delete_comment(request, comment_id):
    return DeleteCommentView.as_view()(request, comment_id=comment_id)

@login_required(login_url='/login')
def manage_tags(request):
    return ManageTagsView.as_view()(request)

@login_required(login_url='/login')
def tag_posts(request, tag_name):
    return TagPostsView.as_view()(request, tag_name=tag_name)

@login_required(login_url='/login')
def delete_tag(request, tag_id):
    return DeleteTagView.as_view()(request, tag_id=tag_id)

@login_required(login_url='/login')
def bookmark(request, id):
    return BookmarkView.as_view()(request, id=id)

@login_required(login_url='/login')
def bookmarks(request):
    return BookmarksView.as_view()(request)