from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from blog_app.models import UserProfile,Blogs,Comments

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following",)
        widgets={
            "date_of_birth":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class ProfilepicUpdateForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            "profile_pic"
        ]
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control"})
        }


class PasswordResetForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField()

class BlogForm(ModelForm):
    class Meta:
        model= Blogs
        fields=[
            "title",
            "description",
            "image"
        ]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields=["comment"]

        widgets = {
            "comment": forms.TextInput(attrs={"class": "form-control"}),
        }
