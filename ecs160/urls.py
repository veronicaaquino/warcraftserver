"""ecs160 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^warcraft/', include('warcraft.urls', namespace="warcraft")),
    url(r'^/$', include('warcraft.urls', namespace="warcraft")),
    url(r'', include('warcraft.urls', namespace="warcraft")),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'warcraft.views.login'),
    url(r'^accounts/auth/$', 'warcraft.views.auth_view'),
    url(r'^accounts/logout/$', 'warcraft.views.logout'),
    url(r'^accounts/loggedin/$', 'warcraft.views.loggedin'),
    url(r'^accounts/invalid/$', 'warcraft.views.invalid_login'),
    url(r'^accounts/register/$', 'warcraft.views.register_user'),
    url(r'^accounts/register_success/$', 'warcraft.views.register_success'),
    url(r'^accounts/internalLogin/$', 'warcraft.views.internalLogin'),
    url(r'^accounts/edit/$', 'warcraft.views.edit_userProfile'),
    url(r'^accounts/edit_success', 'warcraft.views.edit_success'),
    url(r'^accounts/change_password/$', 'warcraft.views.change_password'),
    url(r'^accounts/change_password_success', 'warcraft.views.change_password_success'),
    url(r'^accounts/recover_password/', 'warcraft.views.recover_password'),
    url(r'^accounts/recovery_email_sent/','warcraft.views.edit_success'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)