from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Profile, Post, Comment, Tag

username_validator = RegexValidator(
    r'^[a-zA-Z0-9._]{3,}$',
    'Username can only contain letters, numbers, dots and underscores, minimum 3 characters.'
)

password_validator = RegexValidator(
    r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
    'Password must have at least 8 characters, including both letters and numbers.'
)

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        validators=[username_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'signup-username'
        })
    )
    password = forms.CharField(
        required=True,
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'signup-password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'login-username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'login-password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'rememberMe'
        })
    )

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '3'  
        }),
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['image', 'caption', 'tags']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Caption...',
                'rows': '3'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Please select an image.")
        return image

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profileimg', 'bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Bio...',
                'rows': '3'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location'
            }),
            'profileimg': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': '2',
                'id': 'commentText'
            })
        }
        labels = {
            'text': ''
        }
