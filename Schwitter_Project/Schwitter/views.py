from django.shortcuts import render, redirect
from Schwitter.models import Comment
from Schwitter.models import Post,UserProfile
from Schwitter.forms import UserForm, UserProfileForm, PostForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def main(request):
    context_dict={}
    #If user logged in
    if request.user:
        #Find posts by friends
        user=request.user
        up=UserProfile.objects.get(user=user)
        comments=[]
        posts=[]
        for friend in up.friends.all():
            posts.append(Post.objects.order_by('time').filter(poster=friend))
            comments.append(Comment.objects.order_by('time').filter(Post=Post.objects.filter(poster=friend)))
        context_dict['posts'] =posts
        context_dict['comments']=comments

    #Handle new post form
    if request.method=='POST':
        form=PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster=UserProfile.objects.get(user=request.user)
            post.save()
            return  HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
    else:
        form = PostForm()
        
    context_dict["form"]=form
    return render(request,'schwitter/home.html',context_dict)

def contact(request):
    context_dict={}
    return render(request, 'schwitter/contact.html',context_dict)

def about(request):
    context_dict={}
    return render(request,'schwitter/about.html',context_dict)

    
def options(request):
    context_dict={}
    return render(request,'schwitter/settings.html',context_dict)

def profile(request, username):
    #Attempt to find user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('/schwitter/')

    #if user is found, send all of the information available to context dict
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({"name": user.username,
                            "following":[]})
    posts = Post.objects.filter(poster=userprofile)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect("profile", user.username)
        else:
            print(form.errors)
    context_dict = {"userprofile": userprofile, "user": user,
                    "form": form,"posts": posts}
    print(userprofile.picture)
    return render(request,'schwitter/user_profile.html',context_dict)

    
"""    context_dict={}
    comments=[]
    posts=Post.objects.order_by('time').filter(poster=user)
    for OP in posts:
        comments.append(Comment.objects.order_by('time').filer(post=OP.post))
    context_dict['posts']=posts
    context_dict['comments']=comments"""


def viewPost(request, post):
    context_dict={}
    posts=Post.object.filter(post=post)
    comments=Comment.object.filter(post=post.post)
    context_dict['posts']=posts
    context_dict['comments']=comments

    # Comment form
    form=comment_form()
    if request.method=='POST':
        form=comment_form(request.POST)
        if form.is_valid():
            if post:
                form.poster=user
                form.post=post
                form.save(commit=True)
                return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
            context_dict['form':form]
    
    response=render(request,'schwitter/view_post.html',context_dict)
    return response

def register(request):
    registered=False
    if request.method == 'POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered =True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()

    return render(request,'schwitter/register.html',{'user_form':user_form,
                                                     'profile_form':profile_form,
                                                     'registered':registered})

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your Schwitter account is disabled.")
        else:
            print("Invalid login details: {0},{1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'schwitter/login.html',{})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'schwitter/change_password.html', {
        'form': form
    })

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def add_post(request):
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            form.poster=UserProfile.objects.get(user=self.request.user)
            form.save(commit=True)
            return  HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
    return render(request,'schwitter/post.html',{'form':form})
