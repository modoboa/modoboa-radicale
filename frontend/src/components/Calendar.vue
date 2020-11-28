<template>
  <div>
    <create-event-form :start="start" :end="end" :allDay="allDay" v-if="showCreateEventForm" :show.sync="showCreateEventForm" @eventCreated="renderEvent"></create-event-form>
    <event-form v-if="showEventForm" :id="currentId" :show.sync="showEventForm" @eventDeleted="deleteEvent"></event-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Calendar } from '@fullcalendar/core'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import { DateTime } from 'luxon'
import CreateEventForm from './CreateEventForm.vue'
import EventForm from './EventForm.vue'
import * as api from '@/api'

export default {
  components: {
    'create-event-form': CreateEventForm,
    'event-form': EventForm
  },
  computed: mapGetters([
    'calendars',
    'sharedCalendars'
  ]),
  data () {
    return {
      allDay: false,
      calendar: undefined,
      currentId: null,
      start: null,
      end: null,
      showCreateEventForm: false,
      showEventForm: false
    }
  },
  created () {
    this.$bus.$on('calendarColorChanged', (calendar) => {
      var calType = (calendar.domain) ? 'shared' : 'user'
      var evtSource = this.calendar.getEventSourceById(`${calType}-${calendar.pk}`)
      evtSource.refetch()
    })
    this.$bus.$on('calendarDeleted', (calendar) => {
      var calType = (calendar.domain) ? 'shared' : 'user'
      var evtSource = this.calendar.getEventSourceById(`${calType}-${calendar.pk}`)
      evtSource.remove()
    })
    this.$bus.$on('eventsImported', (calendar) => {
      var calType = (calendar.domain) ? 'shared' : 'user'
      var evtSource = this.calendar.getEventSourceById(`${calType}-${calendar.pk}`)
      evtSource.refetch()
    })
  },
  mounted () {
    const locale = this.$language.current
    if (locale !== 'en') {
      import(`@fullcalendar/core/locales/${locale}.js`).then((module) => {
        this.loadFullCalendar(module.default)
      })
    } else {
      this.loadFullCalendar()
    }
  },
  watch: {
    calendars: function (value) {
      this.addEventSources(value)
    },
    sharedCalendars: function (value) {
      this.addEventSources(value)
    }
  },
  methods: {
    loadFullCalendar (locale) {
      this.calendar = new Calendar(this.$el, {
        plugins: [timeGridPlugin, dayGridPlugin, interactionPlugin],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        initialView: 'timeGridWeek',
        locale: (locale !== undefined) ? locale : this.$language.current,
        timeZone: 'local',
        selectable: true,
        selectMirror: true,
        editable: true,
        dayMaxEventRows: true,
        select: this.selectCallback,
        eventClick: this.eventClickCallback,
        eventDrop: this.eventDropCallback,
        eventResize: this.eventResizeCallback
      })
      this.calendar.render()
      this.addEventSources(this.calendars)
      this.addEventSources(this.sharedCalendars)
    },
    getEventSourceUrl (calendarPk, type) {
      return `/api/v1/${type}-calendars/${calendarPk}/events/`
    },
    addEventSources (calendars) {
      if (this.calendar === undefined) {
        // Not ready yet...
        return
      }
      for (var calendar of calendars) {
        var calType = (calendar.domain) ? 'shared' : 'user'
        var evtSource = this.calendar.getEventSourceById(`${calType}-${calendar.pk}`)
        if (!evtSource) {
          this.calendar.addEventSource({
            id: `${calType}-${calendar.pk}`,
            url: this.getEventSourceUrl(calendar.pk, calType)
          })
        }
      }
    },
    selectCallback (info) {
      this.start = info.start
      this.end = info.end
      this.allDay = info.allDay
      this.showCreateEventForm = true
    },
    closeCreateEventForm () {
      this.showCreateEventForm = false
    },
    renderEvent (event) {
      this.calendar.addEvent(event, true)
    },
    eventClickCallback (info) {
      var evtCalendar = info.event.extendedProps.calendar
      var calType = (evtCalendar.domain) ? 'shared' : 'user'
      this.$router.push({
        name: 'EditEvent',
        params: {
          calendar_type: calType,
          calendar_pk: evtCalendar.pk,
          pk: info.event.id
        }
      })
    },
    updateEventDates (calEvent) {
      var data = {
        start: calEvent.start,
        end: calEvent.end
      }
      var evtCalendar = calEvent.extendedProps.calendar
      if (calEvent.allDay) {
        const end = DateTime.fromJSDate(data.start)
        end.plus({ days: 1 })
        data.start.setHours(0, 0, 0)
        data.end = end
        data.allDay = calEvent.allDay
      } else if (!calEvent.hasEnd) {
        const end = DateTime.fromJSDate(data.start)
        end.plus({ hours: 1 })
        data.end = end
      }
      api.patchEvent(evtCalendar, calEvent.id, data).then(response => {
        this.$notify({
          group: 'default',
          title: this.$gettext('Success'),
          type: 'success',
          text: this.$gettext('Event updated')
        })
      })
    },
    eventDropCallback (info) {
      this.updateEventDates(info.event)
    },
    eventResizeCallback (info) {
      this.updateEventDates(info.event)
    },
    deleteEvent (id) {
      this.calendar.removeEvents(id)
    }
  }
}
</script>

<style src="@fullcalendar/timegrid/main.css" />
