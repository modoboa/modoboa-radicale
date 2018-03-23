"""Calendar serializers."""

from django.utils.translation import ugettext as _

from rest_framework import serializers

from modoboa.admin import models as admin_models
from modoboa.lib import fields as lib_fields

from . import backends
from . import models


class UserCalendarSerializer(serializers.ModelSerializer):
    """User calendar serializer."""

    class Meta:
        model = models.UserCalendar
        fields = ("pk", "name", "color", "path")
        read_only_fields = ("pk", "path", )

    def create(self, validated_data):
        """Use current user."""
        request = self.context["request"]
        calendar = models.UserCalendar.objects.create(
            mailbox=request.user.mailbox, **validated_data)
        backend = backends.get_backend_from_request(
            "caldav_", request)
        backend.create_calendar(calendar.url)
        return calendar


class AttendeeSerializer(serializers.Serializer):
    """Attendee serializer."""

    display_name = serializers.CharField()
    email = serializers.EmailField()


class EventSerializer(serializers.Serializer):
    """Base event serializer (fullcalendar output)."""

    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    allDay = serializers.BooleanField(default=False)
    color = serializers.CharField(read_only=True)
    description = serializers.CharField(required=False)

    attendees = AttendeeSerializer(many=True, required=False)


class ROEventSerializer(EventSerializer):
    """Event serializer for read operations."""

    calendar = UserCalendarSerializer()


class WritableEventSerializer(EventSerializer):
    """Event serializer for write operations."""

    calendar = serializers.PrimaryKeyRelatedField(
        queryset=models.UserCalendar.objects.none())

    def validate(self, data):
        """Make sure dates are present with allDay flag."""
        errors = {}
        if "allDay" in data:
            if "start" not in data:
                errors["start"] = _("This field is required.")
            if "end" not in data:
                errors["end"] = _("This field is required.")
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def __init__(self, *args, **kwargs):
        """Set calendar list."""
        super(EventSerializer, self).__init__(*args, **kwargs)
        self.fields["calendar"].queryset = (
            models.UserCalendar.objects.filter(
                mailbox__user=self.context["request"].user)
        )


class MailboxSerializer(serializers.ModelSerializer):
    """Mailbox serializer."""

    pk = serializers.IntegerField()
    full_address = lib_fields.DRFEmailFieldUTF8()

    class Meta:
        model = admin_models.Mailbox
        fields = ("pk", "full_address")
        read_only_fields = ("pk", "full_address", )


class AccessRuleSerializer(serializers.ModelSerializer):
    """AccessRule serializer."""

    mailbox = MailboxSerializer()

    class Meta:
        model = models.AccessRule
        fields = ("pk", "mailbox", "calendar", "read", "write")

    def create(self, validated_data):
        """Create access rule."""
        mailbox = validated_data.pop("mailbox")
        rule = models.AccessRule(**validated_data)
        rule.mailbox_id = mailbox["pk"]
        rule.save()
        return rule

    def update(self, instance, validated_data):
        """Update access rule."""
        mailbox = validated_data.pop("mailbox")
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.mailbox_id = mailbox["pk"]
        instance.save()
        return instance
