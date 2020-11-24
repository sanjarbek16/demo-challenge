"""challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import challenges.views as challenges_views
import users.views as users_views
import activities.views as activities_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users_views.home, name='home'),
    path('challenges/', include('challenges.urls')),
    path('accounts/', include('allauth.urls')),
    path('c/join-challenge/', challenges_views.join_challenge, name='join_challenge'),
    path('c/invite/', challenges_views.challenge_invite, name='challenge_invite'),
    path('settings/', users_views.settings, name='settings'),
    path('notifications/', activities_views.notifications, name='notifications'),
    re_path(r'^(?P<username>[\w.@]+)/$', users_views.profile, name='profile'),
    re_path(r'^(?P<username>[\w.@]+)/followers/$', users_views.profile_followers, name='profile_followers'),
    re_path(r'^(?P<username>[\w.@]+)/following/$', users_views.profile_following, name='profile_following'),
    re_path(r'^(?P<username>[\w.@]+)/info/$', users_views.profile_info, name='profile_info'),
    re_path(r'^(?P<username>[\w.@]+)/challenges/$', users_views.profile_joined_challenges, name='profile_joined_challenges'),
    re_path(r'^users/follow/$', users_views.user_follow, name='user_follow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)