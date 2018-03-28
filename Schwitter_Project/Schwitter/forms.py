from django import forms
from django.contrib.auth.models import User
from Schwitter.models import UserProfile,Post,Comment

class UserForm(forms.ModelForm):
    #form to create a new user
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields = ('username','email','password','first_name', 'last_name',)

class UserProfileForm(forms.ModelForm):
    #form to upload picture to user profile
    class Meta:
        model=UserProfile
        fields=('picture',)

class PostForm(forms.ModelForm):
    #form to create new post
    poster=forms.ModelChoiceField(widget=forms.HiddenInput(),queryset=UserProfile,initial=None)
    class Meta:
        model=Post
        fields = ('title','content',)


class CommentForm(forms.ModelForm):
    #form to create new comment
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    post = forms.ModelChoiceField(widget=forms.HiddenInput(),queryset=Post,initial=None)
    poster = forms.ModelChoiceField(widget=forms.HiddenInput(),queryset=UserProfile,initial=None)
    time=forms.DateTimeField(widget=forms.HiddenInput(),initial=None)
    class Meta:
        model=Comment
        fields = ('content',)
