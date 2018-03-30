"""Radicale urls."""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CalendarDetailView.as_view(),
        name="calendar_detail_view"),
]
