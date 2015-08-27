from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^pergunta/(?P<pk>.*)/(?P<kind>.*)$', views.report_question, name='report_question'),
    url(r'^resposta/(?P<pk>.*)/(?P<kind>.*)$', views.report_answer, name='report_answer'),
    url(r'^comentario/(?P<pk>.*)/(?P<kind>.*)$', views.report_comment, name='report_comment'),
    url(r'^perfil/(?P<pk>.*)/(?P<kind>.*)$', views.report_profile, name='report_profile'),
]
