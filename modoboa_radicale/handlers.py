"""Radicale signals handlers."""

try:
    from secrets import token_hex
except ImportError:
    from os import urandom
    def token_hex(nbytes=None):
        return urandom(nbytes).hex()

from django.db.models import signals
from django.urls import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from modoboa.core import signals as core_signals

from . import models


PERMISSIONS = [
    ("modoboa_radicale", "usercalendar", "add_usercalendar"),
    ("modoboa_radicale", "usercalendar", "change_usercalendar"),
    ("modoboa_radicale", "usercalendar", "delete_usercalendar"),
    ("modoboa_radicale", "sharedcalendar", "add_sharedcalendar"),
    ("modoboa_radicale", "sharedcalendar", "change_sharedcalendar"),
    ("modoboa_radicale", "sharedcalendar", "delete_sharedcalendar")
]

ROLES_PERMISSIONS = {
    "DomainAdmins": PERMISSIONS,
    "Resellers": PERMISSIONS,
    "SimpleUsers": [
        ("modoboa_radicale", "usercalendar", "add_usercalendar"),
        ("modoboa_radicale", "usercalendar", "change_usercalendar"),
        ("modoboa_radicale", "usercalendar", "delete_usercalendar"),
    ]
}


@receiver(core_signals.extra_role_permissions)
def extra_permissions(sender, role, **kwargs):
    """Extra permissions."""
    return ROLES_PERMISSIONS.get(role, [])


@receiver(core_signals.extra_user_menu_entries)
def top_menu(sender, location, user, **kwargs):
    """Add extra menu entries."""
    if location == "top_menu" and hasattr(user, "mailbox"):
        return [
            {"name": "radicale",
             "label": _("Calendars"),
             "url": reverse("modoboa_radicale:calendar_detail_view")}
        ]
    return []


@receiver(signals.pre_save, sender=models.UserCalendar)
def set_user_calendar_path(sender, instance, **kwargs):
    """Set path at creation."""
    if instance.pk:
        return
    instance._path = "{}/{}".format(
        instance.mailbox.full_address, instance.name)
    if not instance.access_token:
        instance.access_token = token_hex(16)


@receiver(signals.pre_save, sender=models.SharedCalendar)
def set_shared_calendar_path(sender, instance, **kwargs):
    """Set path at creation."""
    if instance.pk:
        return
    instance._path = "{}/{}".format(instance.domain.name, instance.name)
    if not instance.access_token:
        instance.access_token = token_hex(16)
