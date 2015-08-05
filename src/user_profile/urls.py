from django.conf.urls import include, url

from user_profile import views

urlpatterns = [
    url(r'^membros/(?P<pk>.*)$', views.public_profile, name='public_profile'),
    url(r'^$', views.user_profile, name='profile'),
]
