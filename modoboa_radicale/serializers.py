"""Calendar serializers."""

from rest_framework import serializers

from . import models


class UserCalendarSerializer(serializers.ModelSerializer):
    """User calendar serializer."""

    class Meta:
        model = models.UserCalendar
        fields = ("pk", "name", "color", "path")
        read_only_fields = ("pk", "path", )

    def create(self, validated_data):
        """Use current user."""
        user = self.context["request"].user
        return models.UserCalendar.objects.create(
            mailbox=user.mailbox, **validated_data)


class EventSerializer(serializers.Serializer):
    """Event serializer (fullcalendar output)."""

    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    color = serializers.CharField(read_only=True)

    description = serializers.CharField(required=False)
