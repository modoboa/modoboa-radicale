"""Radicale extension models."""

from __future__ import unicode_literals

import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.translation import ugettext as _

from modoboa.admin.models import Domain, Mailbox

from modoboa.lib import exceptions as lib_exceptions
from modoboa.parameters import tools as param_tools


@python_2_unicode_compatible
class Calendar(models.Model):
    """Abstract calendar definition."""

    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default="#3a87ad")
    _path = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return smart_text(self.name)

    @property
    def path(self):
        """Return the calendar path."""
        return self._path

    @property
    def url(self):
        """Return the calendar URL."""
        if not hasattr(self, "_url"):
            server_location = param_tools.get_global_parameter(
                "server_location")
            if not server_location:
                raise lib_exceptions.InternalError(
                    _("Server location is not set, please fix it."))
            self._url = os.path.join(server_location, self._path)
        return self._url

    @property
    def tags(self):
        """Return calendar tags."""
        raise NotImplementedError

    @property
    def owner(self):
        """Return calendar owner."""
        raise NotImplementedError


class UserCalendarManager(models.Manager):
    """Custom UserCalendar manager."""

    def get_for_admin(self, admin):
        """Return the list of calendars this admin can access.

        :param ``core.User`` admin: administrator
        """
        domains = Domain.objects.get_for_admin(admin)
        return self.get_queryset().filter(mailbox__domain__in=domains)


class UserCalendar(Calendar):
    """User calendar.

    We associate the calendar to a mailbox because we need to access
    the related domain.

    """

    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)

    objects = UserCalendarManager()

    class Meta(Calendar.Meta):
        db_table = "radicale_usercalendar"

    @property
    def owner(self):
        return self.mailbox.user


class SharedCalendarManager(models.Manager):
    """Custom SharedCalendar manager."""

    def get_for_admin(self, admin):
        """Return the list of calendars this admin can access.

        :param ``core.User`` admin: administrator
        """
        domains = Domain.objects.get_for_admin(admin)
        return self.get_queryset().filter(domain__in=domains)


class SharedCalendar(Calendar):
    """Shared calendar.

    A shared calendar is associated to a domain and is readable and
    writable by all domain members.

    """

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    objects = SharedCalendarManager()

    class Meta(Calendar.Meta):
        db_table = "radicale_sharedcalendar"

    @property
    def owner(self):
        """Return calendar owner."""
        return self.domain


@python_2_unicode_compatible
class AccessRule(models.Model):
    """Access rules to user calendars."""

    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    calendar = models.ForeignKey(UserCalendar, related_name="rules",
                                 on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('mailbox', 'calendar')
        db_table = "radicale_accessrule"

    def __str__(self):
        access = "r" if self.read else ""
        access += "w" if self.write else ""
        return smart_text(
            "%s access rule to %s -> %s"
            % (self.mailbox, self.calendar, access if access else "no access")
        )
