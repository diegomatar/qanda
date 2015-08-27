from django.conf.urls import include, url

from user_profile import views

urlpatterns = [
    url(r'^follow-user/$', views.follow_user, name='follow_user'),
    url(r'^unfollow-user/$', views.unfollow_user, name='unfollow_user'),
    url(r'^editar/$', views.user_profile, name='edit_profile'),
    url(r'^(?P<slug>.*)/seguidores/$', views.user_followers, name='followers'),
    url(r'^(?P<slug>.*)/perguntas/$', views.user_questions, name='questions'),
    url(r'^(?P<slug>.*)/respostas/$', views.user_answers, name='answers'),
    url(r'^(?P<slug>.*)$', views.public_profile, name='profile'),
    
    
    
]
