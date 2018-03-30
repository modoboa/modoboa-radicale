"""CalDAV calendar backend."""

import datetime
import uuid

import caldav
from caldav.elements import dav
import icalendar

from django.utils import timezone
from django.utils.encoding import smart_str

from modoboa.parameters import tools as param_tools

from . import CalendarBackend


class Caldav_Backend(CalendarBackend):
    """CalDAV calendar backend."""

    def __init__(self, username, password, calendar=None):
        """Constructor."""
        super(Caldav_Backend, self).__init__(calendar)
        server_url = param_tools.get_global_parameter("server_location")
        self.client = caldav.DAVClient(
            server_url,
            username=username, password=password)
        if self.calendar:
            self.remote_cal = self.client.calendar(calendar.path)

    def _serialize_event(self, event):
        """Convert a vevent to a dictionary."""
        vevent = event.instance.walk("vevent")[0]
        result = {
            "id": vevent["uid"],
            "title": vevent["summary"],
            "color": self.calendar.color,
            "description": vevent.get("description", ""),
            "calendar": self.calendar,
            "attendees": []
        }
        if isinstance(vevent["dtstart"].dt, datetime.datetime):
            all_day = False
            start = vevent["dtstart"].dt
            end = vevent["dtend"].dt
        else:
            tz = timezone.get_current_timezone()
            all_day = True
            start = tz.localize(
                datetime.datetime.combine(
                    vevent["dtstart"].dt, datetime.time.min))
            end = tz.localize(
                datetime.datetime.combine(
                    vevent["dtend"].dt, datetime.time.min))
        result.update({
            "allDay": all_day,
            "start": start,
            "end": end
        })
        attendees = vevent.get("attendee", [])
        if isinstance(attendees, icalendar.vCalAddress):
            attendees = [attendees]
        for attendee in attendees:
            result["attendees"].append({
                "display_name": attendee.params.get("cn"),
                "email": smart_str(attendee).replace("MAILTO:", "")
            })
        return result

    def create_calendar(self, url):
        """Create a new calendar."""
        self.client.mkcalendar(url)

    def rename_calendar(self, calendar):
        """Rename an existing calendar."""
        remote_cal = self.client.calendar(calendar.path)
        remote_cal.set_properties([dav.DisplayName(calendar.name)])

    def create_event(self, data):
        """Create a new event."""
        uid = uuid.uuid4()
        cal = icalendar.Calendar()
        evt = icalendar.Event()
        evt.add("uid", uid)
        evt.add("summary", data["title"])
        if not data["allDay"]:
            evt.add("dtstart", data["start"])
            evt.add("dtend", data["end"])
        else:
            evt.add("dtstart", data["start"].date())
            evt.add("dtend", data["end"].date())
        cal.add_component(evt)
        self.remote_cal.add_event(cal)
        return uid

    def update_event(self, uid, original_data):
        """Update an existing event."""
        data = dict(original_data)
        url = "{}/{}.ics".format(self.remote_cal.url.geturl(), uid)
        cal = self.remote_cal.event_by_url(url)
        orig_evt = cal.instance.walk("vevent")[0]
        if "title" in data:
            orig_evt["summary"] = data["title"]
        if "allDay" in data:
            if data["allDay"]:
                data["start"] = data["start"].date()
                data["end"] = data["end"].date()
        if "start" in data:
            del orig_evt["dtstart"]
            orig_evt.add("dtstart", data["start"])
        if "end" in data:
            del orig_evt["dtend"]
            orig_evt.add("dtend", data["end"])
        if "description" in data:
            orig_evt["description"] = data["description"]
        for attdef in data.get("attendees", []):
            attendee = icalendar.vCalAddress(
                "MAILTO:{}".format(attdef["email"]))
            attendee.params["cn"] = icalendar.vText(attdef["display_name"])
            attendee.params["ROLE"] = icalendar.vText('REQ-PARTICIPANT')
            del orig_evt["attendee"]
            orig_evt.add("attendee", attendee, encode=0)
        cal.instance.subcomponents = []
        cal.instance.add_component(orig_evt)
        if "calendar" in data and self.calendar.pk != data["calendar"].pk:
            # Calendar has been changed, remove old event first.
            self.remote_cal.client.delete(url)
            remote_cal = self.client.calendar(data["calendar"].path)
            url = "{}/{}.ics".format(remote_cal.url.geturl(), uid)
        else:
            remote_cal = self.remote_cal
        remote_cal.add_event(cal.instance)
        return uid

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
