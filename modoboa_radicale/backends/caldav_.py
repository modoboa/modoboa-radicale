"""CalDAV calendar backend."""

import caldav
import icalendar
import vobject

from modoboa.parameters import tools as param_tools

from . import CalendarBackend


class Caldav_Backend(CalendarBackend):
    """CalDAV calendar backend."""

    def __init__(self, calendar, username, password):
        """Constructor."""
        super(Caldav_Backend, self).__init__(calendar)
        server_url = param_tools.get_global_parameter("server_location")
        self.client = caldav.DAVClient(
            server_url,
            username=username, password=password)
        self.remote_cal = self.client.calendar(calendar.path)

    def _serialize_event(self, event):
        """Convert a vevent to a dictionary."""
        vevent = event.instance.walk("vevent")[0]
        result = {
            "id": vevent["uid"],
            "title": vevent["summary"],
            "start": vevent["dtstart"].dt,
            "end": vevent["dtend"].dt,
            "color": self.calendar.color,
            "description": vevent.get("description", "")
        }
        return result

    def create_event(self, data):
        """Create a new event."""
        cal = icalendar.Calendar()
        evt = icalendar.Event()
        evt.add("summary", data["title"])
        evt.add("dtstart", data["start"])
        evt.add("dtend", data["end"])
        cal.add_component(evt)
        # ical.vevent.add("description").value = data["description"]
        event = self.remote_cal.add_event(cal.to_ical())
        return event.instance.walk("vevent")[0]["uid"]

    def get_event(self, uid):
        """Retrieve and event using its uid."""
        url = "{}/{}.ics".format(self.remote_cal.url.geturl(), uid)
        event = self.remote_cal.event_by_url(url)
        return self._serialize_event(event)

    def get_events(self, start, end):
        """Retrieve a list of events."""
        orig_events = self.remote_cal.date_search(start, end)
        events = []
        for event in orig_events:
            events.append(self._serialize_event(event))
        return events

    def delete_event(self, uid):
        """Delete an event using its uid."""
        url = "{}/{}.ics".format(self.remote_cal.url.geturl(), uid)
        self.remote_cal.client.delete(url)
