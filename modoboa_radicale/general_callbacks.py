"""
General callbacks.
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from modoboa.lib import events

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


@events.observe("GetExtraRolePermissions")
def extra_permissions(rolename):
    """Extra permissions."""
    return ROLES_PERMISSIONS.get(rolename, [])


@events.observe("UserMenuDisplay")
def top_menu(target, user):
    if target == "top_menu":
        return [
            {"name": "radicale",
             "label": _("Calendars"),
             "url": reverse('modoboa_radicale:index')}
        ]
    return []
