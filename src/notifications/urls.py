from django.conf.urls import include, url

from notifications import views

urlpatterns = [
    url(r'^todas$', views.view_notification, name='view_notification'),
    url(r'^marcar_lida/(?P<kind>.*)/(?P<pk>.*)$', views.mark_as_read, name='mark_as_read'),
    url(r'^marcar_todas_lidas/$', views.mark_all_read, name='mark_all_read'),
    
]
