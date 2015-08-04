from django.conf.urls import include, url

from user_profile import views

urlpatterns = [
    url(r'^$', views.user_profile, name='profile'),
]
