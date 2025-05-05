from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Profile, Post

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
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        required=True,
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
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
