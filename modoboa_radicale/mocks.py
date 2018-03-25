"""Radicale test mocks."""


class DAVClientMock(object):
    """Mock class for DAVClient instance."""

    def mkcalendar(self, url):
        return True
