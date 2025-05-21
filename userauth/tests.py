from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Post, LikePost, Followers, Comment, Tag, Bookmark
import uuid
import tempfile
from PIL import Image
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

class ModelTestCase(TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='12345test'
        )
        
        self.test_profile = Profile.objects.create(
            user=self.test_user,
            id_user=self.test_user.id,
            bio='Test bio',
            location='Test location'
        )
        
        self.test_tag = Tag.objects.create(name='testtag')
        
        self.image = self.create_temporary_image()
        self.test_post = Post.objects.create(
            user=self.test_user.username,
            image=self.image,
            caption='Test caption',
            created_at=timezone.now()
        )
        self.test_post.tags.add(self.test_tag)
        
        self.test_like = LikePost.objects.create(
            post_id=str(self.test_post.id),
            username=self.test_user.username
        )
        
        self.test_comment = Comment.objects.create(
            post=self.test_post,
            user=self.test_user.username,
            text='Test comment',
            created_at=timezone.now()
        )
        
        self.follower_user = User.objects.create_user(
            username='followeruser', 
            password='12345test'
        )
        self.test_follower = Followers.objects.create(
            follower=self.follower_user.username,
            user=self.test_user.username
        )
        
        self.test_bookmark = Bookmark.objects.create(
            user=self.test_user.username,
            post=self.test_post,
            created_at=timezone.now()
        )
    
    def create_temporary_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (100, 100), color='red')
            image.save(f, 'PNG')
            f.seek(0)
            return SimpleUploadedFile(f.name, f.read(), content_type='image/png')
    
    def tearDown(self):
        try:
            os.unlink(self.image.path)
        except:
            pass
    
    def test_profile_model(self):
        self.assertEqual(str(self.test_profile), 'testuser')
        self.assertEqual(self.test_profile.bio, 'Test bio')
        self.assertEqual(self.test_profile.location, 'Test location')
    
    def test_tag_model(self):
        self.assertEqual(str(self.test_tag), 'testtag')
        self.assertTrue(self.test_tag.posts.filter(id=self.test_post.id).exists())
    
    def test_post_model(self):
        self.assertEqual(str(self.test_post), 'testuser')
        self.assertEqual(self.test_post.caption, 'Test caption')
        self.assertEqual(self.test_post.no_of_likes, 0)
        self.assertTrue(self.test_post.tags.filter(name='testtag').exists())
    
    def test_like_post_model(self):
        self.assertEqual(str(self.test_like), 'testuser')
        self.assertEqual(self.test_like.post_id, str(self.test_post.id))
    
    def test_comment_model(self):
        self.assertTrue(str(self.test_comment).startswith('testuser on'))
        self.assertEqual(self.test_comment.text, 'Test comment')
        self.assertEqual(self.test_comment.post, self.test_post)
    
    def test_follower_model(self):
        self.assertEqual(str(self.test_follower), 'testuser')
        self.assertEqual(self.test_follower.follower, 'followeruser')
    
    def test_bookmark_model(self):
        self.assertTrue(str(self.test_bookmark).startswith('testuser bookmarked'))
        self.assertEqual(self.test_bookmark.post, self.test_post)


class ViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='12345test'
        )
        
        self.test_profile = Profile.objects.create(
            user=self.test_user,
            id_user=self.test_user.id,
            bio='Test bio',
            location='Test location'
        )
        
        self.test_tag = Tag.objects.create(name='testtag')
        
        self.image = self.create_temporary_image()
        self.test_post = Post.objects.create(
            user=self.test_user.username,
            image=self.image,
            caption='Test caption',
            created_at=timezone.now()
        )
        self.test_post.tags.add(self.test_tag)
        
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.home_url = reverse('home')
        self.profile_url = reverse('profile', args=[self.test_user.username])
        self.post_detail_url = reverse('post-detail', args=[str(self.test_post.id)])
        self.like_url = reverse('like-post', args=[str(self.test_post.id)])
        self.explore_url = reverse('explore')
        
        self.signup_data = {
            'username': 'newuser',
            'password': 'Pass1234',
            'password2': 'Pass1234',
        }
        
        self.login_data = {
            'username': 'testuser',
            'password': '12345test',
        }
        
        self.post_data = {
            'caption': 'New test post',
            'tags': [self.test_tag.id],
        }
    
    def create_temporary_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (100, 100), color='red')
            image.save(f, 'PNG')
            f.seek(0)
            return SimpleUploadedFile(f.name, f.read(), content_type='image/png')
    
    def tearDown(self):
        try:
            os.unlink(self.image.path)
        except:
            pass
    
    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, self.login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_failure(self):
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
    
    def test_home_view_unauthenticated(self):
        response = self.client.get(self.home_url)
        login_url_with_next = '/login?next=/'
        self.assertRedirects(response, login_url_with_next, fetch_redirect_response=False)
    
    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertIn('user_profile', response.context)
    
    def test_post_detail_view_authenticated(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertIn('post', response.context)
    
    def test_like_post_view_authenticated(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(self.like_url, HTTP_REFERER=self.home_url)
        
        updated_post = Post.objects.get(id=self.test_post.id)
        self.assertEqual(updated_post.no_of_likes, 1)
        
        self.assertTrue(LikePost.objects.filter(
            post_id=str(self.test_post.id),
            username='testuser'
        ).exists())


class FormTestCase(TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='12345test'
        )
        
        self.test_profile = Profile.objects.create(
            user=self.test_user,
            id_user=self.test_user.id,
            bio='Test bio',
            location='Test location'
        )
        
        self.test_tag = Tag.objects.create(name='testtag')
        
        self.valid_signup_data = {
            'username': 'validuser',
            'password': 'Valid1234',
            'password2': 'Valid1234',
        }
        
        self.valid_login_data = {
            'username': 'testuser',
            'password': '12345test',
        }
        
        self.valid_profile_data = {
            'bio': 'New test bio',
            'location': 'New test location',
        }
        
        self.valid_comment_data = {
            'text': 'New test comment',
        }
        
        self.invalid_signup_data = {
            'username': 'in',
            'password': '1234',
            'password2': '1234',
        }
        
        self.invalid_login_data = {
            'username': '',
            'password': '',
        }
    
    def test_signup_form_valid_data(self):
        from .forms import SignUpForm
        form = SignUpForm(data=self.valid_signup_data)
        self.assertTrue(form.is_valid())
    
    def test_signup_form_invalid_data(self):
        from .forms import SignUpForm
        form = SignUpForm(data=self.invalid_signup_data)
        self.assertFalse(form.is_valid())
    
    def test_login_form_valid_data(self):
        from .forms import LoginForm
        form = LoginForm(data=self.valid_login_data)
        self.assertTrue(form.is_valid())
    
    def test_login_form_invalid_data(self):
        from .forms import LoginForm
        form = LoginForm(data=self.invalid_login_data)
        self.assertFalse(form.is_valid())
    
    def test_profile_form_valid_data(self):
        from .forms import ProfileForm
        form = ProfileForm(data=self.valid_profile_data, instance=self.test_profile)
        self.assertTrue(form.is_valid())
    
    def test_comment_form_valid_data(self):
        from .forms import CommentForm
        form = CommentForm(data=self.valid_comment_data)
        self.assertTrue(form.is_valid())


class URLTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='12345test'
        )
        
        self.test_post = Post.objects.create(
            id=uuid.uuid4(),
            user=self.test_user.username,
            caption='Test caption',
            image='post_images/test.jpg',
            created_at=timezone.now()
        )
        
        self.test_tag = Tag.objects.create(name='testtag')
        
    def test_login_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        
    def test_signup_url(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        
    def test_home_url_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login?next=/', fetch_redirect_response=False)
        
    def test_home_url_authenticated(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_logout_url(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        
    def test_profile_url(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(f'/profile/{self.test_user.username}')
        self.assertEqual(response.status_code, 200)
        
    def test_post_detail_url(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(f'/post/{self.test_post.id}')
        self.assertEqual(response.status_code, 200)
        
    def test_tag_posts_url(self):
        self.client.login(username='testuser', password='12345test')
        response = self.client.get(f'/tag/{self.test_tag.name}/')
        self.assertEqual(response.status_code, 200)