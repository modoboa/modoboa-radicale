"""Radicale extension unit tests."""

import mock
import os
import tempfile

try:
    from configparser import ConfigParser
except ImportError:
    # SafeConfigParser (py2) == ConfigParser (py3)
    from ConfigParser import SafeConfigParser as ConfigParser

from django.urls import reverse
from django.utils import six
from django.core import management

from modoboa.core import models as core_models
from modoboa.lib.tests import ModoTestCase, ModoAPITestCase

from modoboa.admin.factories import populate_database
from modoboa.admin.models import Mailbox

from . import factories
from . import models
from . import mocks


class AccessRuleTestCase(ModoTestCase):

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(AccessRuleTestCase, cls).setUpTestData()
        populate_database()

    def setUp(self):
        """Initialize tests."""
        super(AccessRuleTestCase, self).setUp()
        self.rights_file_path = tempfile.mktemp()
        self.set_global_parameter(
            "rights_file_path", self.rights_file_path, app="modoboa_radicale")

    def tearDown(self):
        os.unlink(self.rights_file_path)

    def test_rights_file_generation(self):
        mbox = Mailbox.objects.get(address="admin", domain__name="test.com")
        cal = factories.UserCalendarFactory(mailbox=mbox)

        factories.AccessRuleFactory(
            mailbox=Mailbox.objects.get(
                address="user", domain__name="test.com"),
            calendar=cal, read=True)
        management.call_command("generate_rights", verbosity=False)

        cfg = ConfigParser()
        with open(self.rights_file_path) as fpo:
            if six.PY3:
                cfg.read_file(fpo)
            else:
                cfg.readfp(fpo)

        # Check mandatory rules
        self.assertTrue(cfg.has_section("domain-shared-calendars"))
        self.assertTrue(cfg.has_section("owners-access"))

        # Check user-defined rules
        section = "user@test.com-to-User calendar 0-acr"
        self.assertTrue(cfg.has_section(section))
        self.assertEqual(cfg.get(section, "user"), "user@test.com")
        self.assertEqual(
            cfg.get(section, "collection"),
            "admin@test.com/User calendar 0"
        )
        self.assertEqual(cfg.get(section, "permission"), "r")

        # Call a second time
        management.call_command("generate_rights", verbosity=False)

    def test_rights_file_generation_with_admin(self):
        self.set_global_parameter(
            "allow_calendars_administration", True, app="modoboa_radicale")
        management.call_command("generate_rights", verbosity=False)
        cfg = ConfigParser()
        with open(self.rights_file_path) as fpo:
            if six.PY3:
                cfg.read_file(fpo)
            else:
                cfg.readfp(fpo)

        # Check mandatory rules
        self.assertTrue(cfg.has_section("domain-shared-calendars"))
        self.assertTrue(cfg.has_section("owners-access"))

        # Super admin rules
        section = "sa-admin-acr"
        self.assertTrue(cfg.has_section(section))

        # Domain admin rules
        for section in ["da-admin@test.com-to-test.com-acr",
                        "da-admin@test2.com-to-test2.com-acr"]:
            self.assertTrue(cfg.has_section(section))


class UserCalendarViewSetTestCase(ModoAPITestCase):
    """UserCalendar viewset tests."""

    @classmethod
    def setUpTestData(cls):
        super(UserCalendarViewSetTestCase, cls).setUpTestData()
        populate_database()
        cls.account = core_models.User.objects.get(username="user@test.com")
        cls.calendar = factories.UserCalendarFactory(
            mailbox=cls.account.mailbox)
        cls.admin_account = core_models.User.objects.get(
            username="admin@test.com")
        cls.calendar2 = factories.UserCalendarFactory(
            mailbox=cls.admin_account.mailbox)

    def setUp(self):
        """Initiate test context."""
        self.client.force_login(self.account)
        self.set_global_parameter("server_location", "http://localhost:5232")

    def test_get_calendars(self):
        """List or retrieve calendars."""
        url = reverse("api:user-calendar-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        url = reverse("api:user-calendar-detail", args=[self.calendar.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @mock.patch("caldav.DAVClient")
    def test_create_calendar(self, client_mock):
        """Create a new calendar."""
        client_mock.return_value = mocks.DAVClientMock()
        data = {"username": "user@test.com", "password": "toto"}
        response = self.client.post(reverse("core:login"), data)

        data = {
            "name": "Test calendar",
            "color": "#ffffff"
        }
        url = reverse("api:user-calendar-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_calendar(self):
        """Update existing calendar."""
        data = {"name": "Modified calendar", "color": "#ffffff"}
        url = reverse("api:user-calendar-detail", args=[self.calendar.pk])
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        oldpath = self.calendar.path
        self.calendar.refresh_from_db()
        self.assertEqual(self.calendar.name, data["name"])
        self.assertEqual(self.calendar.path, oldpath)

    def test_delete_calendar(self):
        """Delete existing calendar."""
        url = reverse("api:user-calendar-detail", args=[self.calendar.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(models.UserCalendar.DoesNotExist):
            self.calendar.refresh_from_db()


class AccessRuleViewSetTestCase(ModoAPITestCase):
    """AccessRule viewset tests."""

    @classmethod
    def setUpTestData(cls):
        super(AccessRuleViewSetTestCase, cls).setUpTestData()
        populate_database()
        cls.account = core_models.User.objects.get(username="user@test.com")
        cls.calendar = factories.UserCalendarFactory(
            name="MyCal", mailbox=cls.account.mailbox)

    def setUp(self):
        """Initiate test context."""
        self.client.force_login(self.account)

    def test_create_accessrule(self):
        admin_mb = (
            core_models.User.objects.get(username="admin@test.com").mailbox)
        data = {
            "mailbox": {
                "pk": admin_mb.pk,
                "full_address": admin_mb.full_address
            },
            "read": True,
            "calendar": self.calendar.pk
        }
        url = reverse("api:access-rule-list")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, 201)
