from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import UserForm, UserProfileForm, EditUserForm, ChangePasswordForm
from .models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required

import re
media = '/home/vsaquino/ecs160web/ecs160/media'
# Create your views here.

def index(request):
    template = loader.get_template('warcraft/index.html')
    return HttpResponse(template.render())
    

def prototype_form(request):
    template = loader.get_template('warcraft/prototype_form.html')
    return HttpResponse(template.render())

def prototype(request):
    error = False
    message=""
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
            message = "BAD INPUT"
            return render(request, 'warcraft/prototype_form.html', {'error':error, 'message':message})
        else:
            message = '%s' %request.GET['q']
            if message == "":
                message = "BAD INPUT"
                return render(request, 'warcraft/prototype_form.html', {'error':True, 'message':message})
            else:
                return render(request, 'warcraft/prototype_form.html', {'error':error, 'message':message})
    else:
        return render(request, 'warcraft/prototype_form.html', {'error':error, 'message':message})


def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('warcraft/login.html', c)

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')
        
def logout(request):
    auth.logout(request)
    return render_to_response('warcraft/logout.html')

@login_required  
def loggedin(request):
    profile = request.user.userprofile
    picture = profile.picture
    return render(request, 'warcraft/loggedin.html', {'full_name': request.user.username, 'picture':picture})

def invalid_login(request):
    return render_to_response('warcraft/invalid_login.html')

@login_required    
def edit_userProfile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        edit_user_form = EditUserForm(data=request.POST, instance=request.user)
        edit_profile_form = UserProfileForm(data=request.POST, instance=profile)

        if edit_user_form.is_valid() and edit_profile_form.is_valid():
            user = edit_user_form.save()
            user.set_password(user.password)
            user.save()
            profile = edit_profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
              profile.picture = request.FILES['picture']
            profile.save()
        else:
            print(edit_user_form.errors, edit_profile_form.errors)
    else:
        edit_user_form = EditUserForm(instance=request.user)
        edit_profile_form = UserProfileForm(instance=profile)

    return render(request, 'warcraft/edit_userProfile.html', {'edit_user_form': edit_user_form, 'edit_profile_form': edit_profile_form})

@login_required
def edit_success (request):
    profile = request.user.userprofile
    request.user.first_name = request.POST.get("first_name", "")
    request.user.last_name = request.POST.get("last_name", "")
    request.user.email = request.POST.get("email", "")
    request.user.save()
    if 'picture' in request.FILES:
      profile.picture = request.FILES['picture']
    profile.save()
    
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    picture = profile.picture
    return render(request, 'warcraft/edit_success.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'picture': picture})
  
@login_required    
def change_password(request):
    if request.method == "POST":
        change_password_form = ChangePasswordForm(data=request.POST, instance=request.user)
        
        if change_password_form.is_valid():
            user = change_password_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print(change_password_form.errors)
    else:
        change_password_form = ChangePasswordForm(instance=request.user)

    return render(request, 'warcraft/change_password.html', {'change_password_form': change_password_form})

@login_required
def change_password_success (request):
    request.user.set_password(request.POST.get("password", ""))
    request.user.save()
    return render(request, 'warcraft/change_password_success.html')
    
  
def register_user(request):
    context = RequestContext(request)
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
              profile.picture = request.FILES['picture']
            profile.save()
            return HttpResponseRedirect('/accounts/register_success')
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('warcraft/register.html', {'user_form': user_form, 'profile_form': profile_form}, context)

def register_success (reqest):
    return render_to_response('warcraft/register_success.html')

def internalLogin (request):
    if request.method == 'GET':
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/loggedin')
        else:
            return HttpResponseRedirect('/accounts/invalid')
        return render(request, 'warcraft/internalLogin.html', {'username': dummy, 'password': passdummy})
        
def recover_password(request):
    return render_to_response('warcraft/change_password.html')

        
        
        