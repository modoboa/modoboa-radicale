"""Calendar viewsets."""

import dateutil

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, response, viewsets

from modoboa.admin import models as admin_models

from . import backends
from . import models
from . import serializers


def parse_date_from_iso(value):
    """Return a tz aware datetime parsed from an ISO date."""
    return dateutil.parser.parse(value)


class UserCalendarViewSet(viewsets.ModelViewSet):
    """Calendar viewset."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserCalendarSerializer

    def get_queryset(self):
        """Filter based on current user."""
        qset = models.UserCalendar.objects.filter(
            mailbox__user=self.request.user)
        return qset


class EventViewSet(viewsets.ViewSet):
    """Event viewset."""

    def create(self, request, calendar_pk):
        """Create new event."""
        serializer = serializers.WritableEventSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        backend = backends.get_backend_from_request(
            "caldav_", request, serializer.validated_data["calendar"])
        uid = backend.create_event(serializer.validated_data)
        event = dict(serializer.validated_data)
        calendar = serializer.validated_data["calendar"]
        event["id"] = uid
        event["color"] = calendar.color
        event["calendar"] = {"pk": calendar.pk}
        return response.Response(event, status=201)

    def update(self, request, pk, calendar_pk):
        """Update existing event."""
        serializer = serializers.WritableEventSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        calendar = models.UserCalendar.objects.get(pk=calendar_pk)
        backend = backends.get_backend_from_request(
            "caldav_", request, calendar)
        uid = backend.update_event(pk, serializer.validated_data)
        event = dict(serializer.data)
        event["id"] = uid
        return response.Response(event, status=200)

    def partial_update(self, request, pk, calendar_pk):
        """Update existing event."""
        serializer = serializers.WritableEventSerializer(
            data=request.data, context={"request": request}, partial=True)
        serializer.is_valid(raise_exception=True)
        calendar = models.UserCalendar.objects.get(pk=calendar_pk)
        backend = backends.get_backend_from_request(
            "caldav_", request, calendar)
        backend.update_event(pk, serializer.validated_data)
        return response.Response(status=200)

    def list(self, request, calendar_pk):
        """Get a list of event."""
        start = request.GET.get("start")
        end = request.GET.get("end")
        if not start or not end:
            return response.Response()
        events = []
        calendar = models.UserCalendar.objects.get(pk=calendar_pk)
        backend = backends.get_backend_from_request(
            "caldav_", request, calendar)
        events += backend.get_events(
            parse_date_from_iso(start), parse_date_from_iso(end))
        serializer = serializers.ROEventSerializer(
            events, many=True, context={"request": request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk, calendar_pk):
        """Get a specific event."""
        calendar = models.UserCalendar.objects.get(pk=calendar_pk)
        backend = backends.get_backend_from_request(
            "caldav_", request, calendar)
        event = backend.get_event(pk)
        serializer = serializers.ROEventSerializer(
            event, context={"request": request})
        return response.Response(serializer.data)

    def destroy(self, request, pk, calendar_pk):
        """Destroy a specific event."""
        calendar = models.UserCalendar.objects.get(pk=calendar_pk)
        backend = backends.get_backend_from_request(
            "caldav_", request, calendar)
        backend.delete_event(pk)
        return response.Response()


class AttendeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Attendee viewset."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AttendeeSerializer

    def list(self, request, *args, **kwargs):
        """Return attendees available for current user."""
        domain_pk = request.user.mailbox.domain_id
        mb_qset = admin_models.Mailbox.objects.filter(
            domain__pk=domain_pk, domain__enabled=True, user__is_active=True
        ).exclude(pk=request.user.mailbox.pk)
        attendees = []
        for mb in mb_qset:
            attendees.append({
                "display_name": mb.user.fullname, "email": mb.full_address})
        serializer = serializers.AttendeeSerializer(
            attendees, many=True, context={"request": request})
        return response.Response(serializer.data)


class MailboxViewSet(viewsets.ReadOnlyModelViewSet):
    """RO mailbox viewset."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MailboxSerializer

    def get_queryset(self):
        """Filter queryset based on current user."""
        domain_pk = self.request.user.mailbox.domain_id
        return admin_models.Mailbox.objects.filter(
            domain__pk=domain_pk, domain__enabled=True, user__is_active=True
        ).exclude(pk=self.request.user.mailbox.pk)


class AccessRuleViewSet(viewsets.ModelViewSet):
    """AccessRule viewset."""

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ("calendar", )
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AccessRuleSerializer

    def get_queryset(self):
        return models.AccessRule.objects.filter(
            calendar__mailbox=self.request.user.mailbox)
