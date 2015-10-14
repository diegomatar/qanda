from django.conf.urls import include, url

from user_profile import views

urlpatterns = [
    url(r'^follow-user/$', views.follow_user, name='follow_user'),
    url(r'^unfollow-user/$', views.unfollow_user, name='unfollow_user'),
    url(r'^add-topic-known/$', views.add_topic_known, name='add-topic-known'),
    url(r'^remove-topic-known/$', views.remove_topic_known, name='remove-topic-known'),
    url(r'^editar-temas-conhecidos/$', views.edit_user_known_topics, name='edit_user_known_topics'),
    url(r'^editar-foto/$', views.edit_user_profile_picture, name='edit_profile_picture'),
    url(r'^editar/$', views.edit_user_profile, name='edit_profile'),
    url(r'^(?P<slug>.*)/seguidores/$', views.user_followers, name='followers'),
    url(r'^(?P<slug>.*)/perguntas/$', views.user_questions, name='questions'),
    url(r'^(?P<slug>.*)/respostas/$', views.user_answers, name='answers'),
    url(r'^(?P<slug>.*)$', views.public_profile, name='profile'),
    
    
    
]
