"""Radicale signals handlers."""

from django.urls import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from modoboa.core import signals as core_signals

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
    "Resellers": PERMISSIONS
}


@receiver(core_signals.extra_role_permissions)
def extra_permissions(sender, role, **kwargs):
    """Extra permissions."""
    return ROLES_PERMISSIONS.get(role, [])


@receiver(core_signals.extra_user_menu_entries)
def top_menu(sender, location, user, **kwargs):
    """Add extra menu entries."""
    if location == "top_menu":
        return [
            {"name": "radicale",
             "label": _("Calendars"),
             "url": reverse('modoboa_radicale:index')}
        ]
    return []
