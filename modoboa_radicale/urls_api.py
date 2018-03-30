"""Radicale urls."""

from rest_framework_nested import routers

from . import viewsets

router = routers.SimpleRouter()
router.register(
    r"user-calendars", viewsets.UserCalendarViewSet,
    base_name="user-calendar")
router.register(
    r"shared-calendars", viewsets.SharedCalendarViewSet,
    base_name="shared-calendar")
router.register(
    r"attendees", viewsets.AttendeeViewSet, base_name="attendee")
router.register(
    r"mailboxes", viewsets.MailboxViewSet, base_name="mailbox")
router.register(
    r"accessrules", viewsets.AccessRuleViewSet, base_name="access-rule")

calendars_router = routers.NestedSimpleRouter(
    router, r"user-calendars", lookup="calendar")
calendars_router.register(
    r"events", viewsets.UserEventViewSet, base_name="event")
shared_calendars_router = routers.NestedSimpleRouter(
    router, r"shared-calendars", lookup="calendar")
shared_calendars_router.register(
    r"events", viewsets.SharedEventViewSet, base_name="event")

urlpatterns = (
    router.urls + calendars_router.urls + shared_calendars_router.urls
)
