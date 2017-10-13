"""Calendar viewsets."""

import dateutil

from django.utils import timezone

from rest_framework import permissions, response, viewsets

from . import backends
from . import models
from . import serializers


def parse_date_from_iso(value):
    """Return a tz aware datetime parsed from an ISO date."""
    return timezone.get_current_timezone().localize(
        dateutil.parser.parse(value))


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

    def create(self, request):
        """Create new event."""
        serializer = serializers.EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        backend = backends.get_backend_from_request("caldav_", request)
        uid = backend.create_event(serializer.validated_data)
        event = dict(serializer.data)
        event["id"] = uid
        return response.Response(event, status=201)

    def list(self, request):
        """Get a list of event."""
        start = request.GET.get("start")
        end = request.GET.get("end")
        if not start or not end:
            return response.Response()
        backend = backends.get_backend_from_request("caldav_", request)
        events = backend.get_events(
            parse_date_from_iso(start), parse_date_from_iso(end))
        serializer = serializers.EventSerializer(events, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk):
        """Get a specific event."""
        backend = backends.get_backend_from_request("caldav_", request)
        event = backend.get_event(pk)
        serializer = serializers.EventSerializer(event)
        return response.Response(serializer.data)

    def destroy(self, request, pk):
        """Destroy a specific event."""
        backend = backends.get_backend_from_request("caldav_", request)
        backend.delete_event(pk)
        return response.Response()
