from django.conf.urls import include, url

from user_profile import views

urlpatterns = [
    url(r'^membros/(?P<pk>.*)$', views.public_profile, name='public_profile'),
    url(r'^follow-user/$', views.follow_user, name='follow_user'),
    url(r'^unfollow-user/$', views.unfollow_user, name='unfollow_user'),
    url(r'^$', views.user_profile, name='profile'),
    
]
