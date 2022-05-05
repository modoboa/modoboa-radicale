"""CalDAV calendar backend."""

import datetime
import uuid

import caldav
from caldav.elements import dav, ical
from caldav import Calendar
from dateutil.relativedelta import relativedelta
import vobject

from django.utils import timezone
from django.utils.encoding import smart_str

from modoboa.parameters import tools as param_tools

from . import CalendarBackend


class Caldav_Backend(CalendarBackend):
    """CalDAV calendar backend."""

    def __init__(self, username, password, calendar=None):
        """Constructor."""
        super().__init__(calendar)
        server_url = smart_str(
            param_tools.get_global_parameter("server_location"))
        self.client = caldav.DAVClient(
            server_url,
            username=username, password=password)
        if self.calendar:
            self.remote_cal = Calendar(self.client, calendar.encoded_path)

    def _serialize_event(
            self,
            vevent,
            start=None,
            end=None,
            all_day: bool = False,
            **kwargs) -> dict:
        """Convert a vevent to a dictionary."""
        description = (
            vevent.description.value
            if "description" in vevent.contents else ""
        )
        event_id = vevent.uid.value
        result = {
            "id": event_id,
            "title": vevent.summary.value,
            "color": self.calendar.color,
            "description": description,
            "calendar": self.calendar,
            "attendees": [],
            # Quick way to disable edition of recurring events until
            # we support it.
            "editable": not kwargs.get("recurring", False),
            **kwargs
        }
        if start is None and end is None:
            start = vevent.dtstart.value
            end = vevent.dtend.value
        if isinstance(start, datetime.datetime):
            all_day = all_day
        else:
            tz = timezone.get_current_timezone()
            all_day = True
            start = tz.localize(
                datetime.datetime.combine(start, datetime.time.min))
            end = tz.localize(
                datetime.datetime.combine(end, datetime.time.min))
        result.update({
            "allDay": all_day,
            "start": start,
            "end": end
        })
        if "attendee" in vevent.contents:
            if "organizer" in vevent.contents:
                organizer = vevent.organizer.value.replace("mailto:", "")
                if organizer != self.calendar.mailbox.full_address:
                    result["editable"] = False
            for attendee in vevent.contents["attendee"]:
                email = (
                    attendee.value
                    .replace("mailto:", "")
                    .replace("MAILTO:", "")
                )
                cn = attendee.params.get("CN")
                result["attendees"].append({
                    "display_name": cn[0] if cn else "",
                    "email": email
                })
        return result

    def _serialize_events(self, event, start, end) -> list:
        """Convert this event to a list of dictionaries.

        In case of recurring event, we will generate as much
        dictionaries as necessary, according to given start and end
        dates.

        """
        tz = timezone.get_current_timezone()
        result = []
        for vevent in event.vobject_instance.vevent_list:
            rruleset = vevent.getrruleset()
            if rruleset:
                all_day = True
                duration = relativedelta(
                    vevent.dtend.value, vevent.dtstart.value)
                if isinstance(vevent.dtstart.value, datetime.datetime):
                    all_day = False
                for date in list(rruleset):
                    if date.tzinfo is None:
                        date = tz.localize(date)
                    if date >= start and date <= end:
                        result += [
                            self._serialize_event(
                                vevent, date, date + duration, all_day=all_day,
                                recurring=True
                            )
                        ]
            else:
                options = {}
                if "recurrence-id" in vevent.contents:
                    # Remove previously expanded event because it has
                    # been overriden
                    recurrence_id = vevent.recurrence_id.value
                    options["recurring"] = True
                    for (pos, item) in enumerate(result):
                        if (
                            item["id"] == vevent.uid.value and
                            item["start"] == recurrence_id
                        ):
                            del result[pos]
                            break
                result += [self._serialize_event(vevent, **options)]
        return result

    def create_calendar(self, url):
        """Create a new calendar."""
        self.client.mkcalendar(url)

    def update_calendar(self, calendar):
        """Update an existing calendar."""
        remote_cal = Calendar(self.client, calendar.encoded_path)
        remote_cal.set_properties([dav.DisplayName(calendar.name),
                                   ical.CalendarColor(calendar.color)])

    def create_event(self, data):
        """Create a new event."""
        uid = uuid.uuid4()
        cal = vobject.iCalendar()
        cal.add("vevent")
        cal.vevent.add("uid").value = str(uid)
        cal.vevent.add("summary").value = data["title"]
        if not data["allDay"]:
            cal.vevent.add("dtstart").value = data["start"]
            cal.vevent.add("dtend").value = data["end"]
        else:
            cal.vevent.add("dtstart").value = data["start"].date()
            cal.vevent.add("dtend").value = data["end"].date()
        self.remote_cal.add_event(cal)
        return uid

    def update_event(self, uid, original_data):
        """Update an existing event."""
        data = dict(original_data)
        url = "{}/{}.ics".format(self.remote_cal.url.geturl(), uid)
        cal = self.remote_cal.event_by_url(url)
        orig_evt = cal.vobject_instance.vevent
        if "title" in data:
            orig_evt.summary.value = data["title"]
        if data.get("allDay"):
            data["start"] = data["start"].date()
            data["end"] = data["end"].date()
        if "start" in data:
            del orig_evt.contents["dtstart"]
            orig_evt.add("dtstart").value = data["start"]
        if "end" in data:
            del orig_evt.contents["dtend"]
            orig_evt.add("dtend").value = data["end"]
        if "description" in data:
            if "description" in orig_evt.contents:
                orig_evt.description.value = data["description"]
            else:
                orig_evt.add("description").value = data["description"]
        if "attendees" in data:
            if "attendee" in orig_evt.contents:
                del orig_evt.contents["attendee"]
            for attdef in data.get("attendees", []):
                attendee = orig_evt.add('attendee')
                attendee.value = "MAILTO:{}".format(attdef["email"])
                attendee.params["CN"] = [attdef["display_name"]]
                attendee.params["ROLE"] = ['REQ-PARTICIPANT']
        if "calendar" in data and self.calendar.pk != data["calendar"].pk:
            # Calendar has been changed, remove old event first.
            self.remote_cal.client.delete(url)
            remote_cal = Calendar(self.client, data["calendar"].encoded_path)
            url = "{}/{}.ics".format(remote_cal.url.geturl(), uid)
        else:
            remote_cal = self.remote_cal
        remote_cal.add_event(cal.instance)
        return uid

    def get_event(self, uid):
        """Retrieve and event using its uid."""
        url = "{}/{}.ics".format(self.remote_cal.url.geturl(), uid)
        event = self.remote_cal.event_by_url(url)
        vevent = event.vobject_instance.vevent
        return self._serialize_event(vevent)

    def get_events(self, start, end):
        """Retrieve a list of events."""
        orig_events = self.remote_cal.date_search(start, end)
        events = []
        for event in orig_events:
            events += self._serialize_events(event, start, end)
        return events

    def delete_event(self, uid):
        """Delete an event using its uid."""
        url = "{}/{}.ics".format(self.remote_cal.url.geturl(), uid)
        self.remote_cal.client.delete(url)

    def import_events(self, fp):
        """Import events from file."""
        content = smart_str(fp.read())
        counter = 0
        for cal in vobject.base.readComponents(content):
            for event in cal.vevent_list:
                ical = vobject.iCalendar()
                ical.add(event)
                self.remote_cal.add_event(ical.serialize())
                counter += 1
        return counter
