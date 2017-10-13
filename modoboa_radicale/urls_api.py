"""Radicale urls."""

from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()
router.register(
    r"user-calendars", viewsets.UserCalendarViewSet, base_name="calendar")
router.register(r"events", viewsets.EventViewSet, base_name="event")
urlpatterns = router.urls
