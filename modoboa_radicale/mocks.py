"""Radicale test mocks."""

from caldav import objects


EV1 = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:20010712T182145Z-123401@example.com
DTSTAMP:20060712T182145Z
DTSTART:20060714T170000Z
DTEND:20060715T040000Z
SUMMARY:Bastille Day Party
END:VEVENT
END:VCALENDAR
"""

EV2 = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:20010712T182145Z-123401@example.com
DTSTAMP:20070712T182145Z
DTSTART:20070714T170000Z
DTEND:20070715T040000Z
SUMMARY:Bastille Day Party +1year
END:VEVENT
END:VCALENDAR
"""


class Url(object):

    def __init__(self, path):
        self.path = path

    def geturl(self):
        return self.path


class Calendar(object):

    def __init__(self, client, path):
        self.url = Url(path)
        self.client = client

    def add_event(self, data):
        return True

    def event_by_url(self, url):
        return objects.Event(data=EV1, parent=self)

    def date_search(self, start, end):
        return [
            objects.Event(data=EV1, parent=self),
            objects.Event(data=EV2, parent=self)
        ]

    def set_properties(self, properties):
        return True


class DAVClientMock(object):
    """Mock class for DAVClient instance."""

    def calendar(self, path):
        return Calendar(self, path)

    def mkcalendar(self, url):
        return True

    def delete(self, url):
        return True
