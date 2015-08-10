from django.conf.urls import include, url

from notifications import views

urlpatterns = [
    url(r'^todas$', views.view_notification, name='view_notification'),
]
