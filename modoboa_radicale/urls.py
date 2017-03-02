"""Radicale urls."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^list/$', views.calendars_page, name="calendars_page"),
    url(r'^user/$', views.new_user_calendar, name='user_calendar_add'),
    url(r'^user/(?P<pk>\d+)/$', views.user_calendar,
        name='user_calendar'),
    url(r'^user/(?P<pk>\d+)/detail/$', views.user_calendar_detail,
        name='user_calendar_detail'),
    url(r'^shared/$', views.new_shared_calendar,
        name='shared_calendar_add'),
    url(r'^shared/(?P<pk>\d+)/$', views.shared_calendar,
        name='shared_calendar'),
    url(r'^shared/(?P<pk>\d+)/detail/$', views.shared_calendar_detail,
        name='shared_calendar_detail'),
    url(r'^usernames/$', views.username_list, name='username_list'),
]
