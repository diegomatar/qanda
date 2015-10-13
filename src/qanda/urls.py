"""qanda URL Configuration

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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from perguntas import views
from user_profile import views as user_profile_views
from user_profile import urls as profile_urls
from notifications import urls as notifications_urls
from report import urls as report_urls

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^pergunta/(?P<slug>.*)$', views.pergunta, name='pergunta'),
    url(r'^perguntar/$', views.perguntar, name='perguntar'),
    url(r'^responder-perguntas/$', views.responder_perguntas, name='responder-perguntas'),
    url(r'^sugerir-pergunta/$', views.suggest_question, name='suggest_question'),
    url(r'^buscar-topicos/$', views.search_topics, name='search_topics'),
    url(r'^criar-topico-conhecimento/$', views.create_topic_known, name='create_topic_known'),
    url(r'^conhecimentos-atuais/$', views.current_known_topics, name='current_known_topics'),
    url(r'^atualiza-sugestoes/$', views.update_topics_sugestion, name='update_topics_sugestion'),
    url(r'^unfollow-question/$', views.unfollow_question, name='unfollow_question'),
    url(r'^follow-tag/$', views.follow_tag, name='follow_tag'),
    url(r'^unfollow-tag/$', views.unfollow_tag, name='unfollow_tag'),
    url(r'^follow-question/$', views.follow_question, name='follow_question'),
    url(r'^responder/(?P<pk>.*)$', views.responder, name='responder'),
    url(r'^perguntar-novamente/(?P<pk>.*)$', views.perguntar_novamente, name='perguntar_novamente'),
    url(r'^pedir-resposta/$', views.ask_to_answer, name='ask_to_answer'),
    url(r'^editar-pergunta/(?P<pk>.*)$', views.edit_question, name='editar_pergunta'),
    url(r'^editar-resposta/(?P<pk>.*)$', views.edit_answer, name='editar_resposta'),
    url(r'^comentar-resposta/(?P<pk>.*)$', views.add_comment, name='add_comment'),
    url(r'^editar-comentario/(?P<pk>.*)$', views.edit_comment, name='edit_comment'),
    url(r'^upvote/$', views.upvote, name='upvote'),
    url(r'^downvote/$', views.downvote, name='downvote'),
    url(r'^resp-upvote/$', views.resp_upvote, name='resp_upvote'),
    url(r'^resp-downvote/$', views.resp_downvote, name='resp_downvote'),
    url(r'^categoria/(?P<slug>.*)$', views.categoria, name='categoria'),
    url(r'^membros/$', user_profile_views.members, name='members'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^conta/', include('allauth.urls')),
    url(r'^reportar/', include(report_urls)),
    url(r'^perfil/', include(profile_urls)),
    url(r'^notificacoes/', include(notifications_urls)),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
