from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^', views.home, name='challenges'),
    re_path(r'^(?P<username>\w+)/$', views.profile, name='profile'),
    re_path(r'^(?P<username>\w+)/followers/$', views.profile_followers, name='profile_followers'),
    re_path(r'^users/follow/$', views.user_follow, name='user_follow'),
]
