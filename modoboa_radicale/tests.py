"""Radicale extension unit tests."""

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

from rest_framework.authtoken.models import Token

from modoboa.core import models as core_models
from modoboa.lib.tests import ModoTestCase, ModoAPITestCase

from modoboa.admin.factories import populate_database
from modoboa.admin.models import Mailbox

from .factories import (
    UserCalendarFactory, SharedCalendarFactory, AccessRuleFactory
)
from .models import UserCalendar, SharedCalendar, AccessRule
from .modo_extension import Radicale


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
        cal = UserCalendarFactory(mailbox=mbox)

        AccessRuleFactory(
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
            "test.com/user/admin/User calendar 0"
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


class AccessRuleViewSetTestCase(ModoAPITestCase):
    """AccessRule viewset tests."""

    @classmethod
    def setUpTestData(cls):
        super(AccessRuleViewSetTestCase, cls).setUpTestData()
        populate_database()
        cls.account = core_models.User.objects.get(username="user@test.com")
        cls.token = Token.objects.create(user=cls.account)
        cls.calendar = UserCalendarFactory(
            name="MyCal", mailbox=cls.account.mailbox)

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
        url = reverse("modoboa_radicale:access-rule-list")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, 201)
