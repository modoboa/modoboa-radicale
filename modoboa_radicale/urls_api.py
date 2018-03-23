"""Radicale urls."""

from rest_framework_nested import routers

from . import viewsets

router = routers.SimpleRouter()
router.register(
    r"user-calendars", viewsets.UserCalendarViewSet, base_name="calendar")
router.register(
    r"attendees", viewsets.AttendeeViewSet, base_name="attendee")
router.register(
    r"mailboxes", viewsets.MailboxViewSet, base_name="mailbox")
router.register(
    r"accessrules", viewsets.AccessRuleViewSet, base_name="access-rule")

calendars_router = routers.NestedSimpleRouter(
    router, r"user-calendars", lookup="calendar")
calendars_router.register(r"events", viewsets.EventViewSet, base_name="event")

urlpatterns = router.urls + calendars_router.urls
