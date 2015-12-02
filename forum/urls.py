from django.conf.urls import include, url, patterns
from forum.models import *

urlpatterns = patterns('forum.views',
    (r"^forum/(\d+)/$", "forum"),
    (r"^thread/(\d+)/$", "thread"),
    (r"^post/(new_thread|reply)/(\d+)/$", "post"),
    (r"^reply/(\d+)/$", "reply"),
    (r"^profile/(\d+)/$", "profile"),
    (r"^new_thread/(\d+)/$", "new_thread"),
    (r"", "main"),
)
