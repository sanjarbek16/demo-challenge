from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.create_challenge, name='create_challenge'),
    re_path(r'^(?P<slug>[-\w]+)/$', views.detail, name='challenge'),
    re_path(r'^(?P<slug>[-\w]+)/leaderboard/$', views.leaderboard, name='leaderboard'),
    re_path(r'^(?P<slug>[-\w]+)/invite/$', views.invite_following, name='leaderboard'),
    re_path(r'^$', views.list, name='challenges'),
]
