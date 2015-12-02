from string import join
from PIL import Image as PImage
from os.path import join as pjoin
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from ecs160.settings import MEDIA_ROOT, MEDIA_URL
from forum.models import *


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["posts", "user"]
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.FileField()
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'picture', 'body']

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def main(request):
    """Main listing."""
    forums = Forum.objects.all()
    return render_to_response("forum/list.html", dict(forums=forums, user=request.user))

def forum(request, pk):
    """Listing of threads in a forum."""
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = mk_paginator(request, threads, 20)
    return render_to_response("forum/forum.html", add_csrf(request, threads=threads, pk=pk))

def thread(request, pk):
    """Listing of posts in a thread."""
    posts = Post.objects.filter(thread=pk).order_by("created")
    posts = mk_paginator(request, posts, 15)
    t = Thread.objects.get(pk=pk)
    return render_to_response("forum/thread.html", add_csrf(request, posts=posts, pk=pk, title=t.title,
                                                           forum_pk=t.forum.pk, media_url=MEDIA_URL))

@login_required
def profile(request, pk):
    """Edit user profile."""
    profile = UserProfile.objects.get(user=pk)
    img = None

    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES, instance=profile)
        if pf.is_valid():
            pf.save()
            # resize and save image under same filename
            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            im = PImage.open(imfn)
            im.thumbnail((160,160), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
    else:
        pf = ProfileForm(instance=profile)

    if profile.avatar:
        img = "/media/" + profile.avatar.name
    return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))

@login_required
def post(request, ptype, pk):
    """Display a post form."""
    action = reverse("forum.views.%s" % ptype, args=[pk])
    if ptype == "new_thread":
        title = "Start New Topic"
        subject = ''
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(pk=pk).title

    return render_to_response("forum/post.html", add_csrf(request, subject=subject, action=action,
                                                          title=title))
def handle_uploaded_file(f):
    #f.save()
    imfn = pjoin(MEDIA_ROOT, f)
    im = PImage.open(imfn)
    im.save(imfn, "JPEG")

def increment_post_counter(request):
    #profile = request.user.userprofile_set.all()[0]
    profile = request.user
    profile.posts += 1
    profile.save()

@login_required
def new_thread(request, pk):
    """Start a new thread."""
    p = request.POST
    if p["subject"] and p["body"]:
        forum = Forum.objects.get(pk=pk)
        thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
        Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse("forum.views.forum", args=[pk]))

@login_required
def reply(request, pk):
    thread = Thread.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        #if form.is_valid():
        if(request.FILES):
            post = Post(thread=thread, picture= request.FILES['picture'], title=request.POST['subject'], body=request.POST['body'], creator=request.user)
            post.save()
        else:
            post = Post(thread=thread, title=request.POST['subject'], body=request.POST['body'], creator=request.user)
            post.save()
        #else:
        #    form = PostForm()
    return HttpResponseRedirect(reverse("forum.views.thread", args=[pk]) + "?page=last")
"""
def reply(request, pk):
    #form = UploadFileForm(request.POST, request.FILES)
    #handle_uploaded_file(request.FILES['image'])
    p = request.POST
    #p = UploadFileForm(request.POST, request.FILES)
    if p["body"]:
        thread = Thread.objects.get(pk=pk)
        post = Post.objects.create(thread=thread, picture=p["attachment"], title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    send_mail("new reply", "new reply on forum", 'chriscraftecs160@gmail.com', [thread.creator.email])
    #return render(request, "forum/test.html", { 'reply': thread.creator })
    return HttpResponseRedirect(reverse("forum.views.thread", args=[pk]) + "?page=last")
"""


def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d
