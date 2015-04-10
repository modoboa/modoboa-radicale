"""Tests runner for modoboa_admin."""

import unittest

from modoboa.lib.test_utils import TestRunnerMixin


class TestRunner(TestRunnerMixin, unittest.TestCase):

    """The tests runner."""

    extension = "modoboa_radicale"
    dependencies = [
        "modoboa_admin"
    ]
