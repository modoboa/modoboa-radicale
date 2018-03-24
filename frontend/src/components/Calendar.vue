<template>
  <div>
    <create-event-form :start="start" :end="end" :allDay="allDay" v-if="showCreateEventForm" :show.sync="showCreateEventForm" @eventCreated="renderEvent"></create-event-form>
    <event-form v-if="showEventForm" :id="currentId" :show.sync="showEventForm" @eventDeleted="deleteEvent"></event-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import $ from 'jquery'
import fullCalendar from 'fullcalendar' // eslint-disable-line no-unused-vars
import 'fullcalendar/dist/locale/fr'
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
            currentId: null,
            start: null,
            end: null,
            showCreateEventForm: false,
            showEventForm: false
        }
    },
    created () {
        this.$bus.$on('calendarColorChanged', (calendar) => {
            var url = this.getEventSourceUrl(calendar.pk)
            this.cal.fullCalendar('refetchEventSources', url)
        })
        this.$bus.$on('calendarDeleted', (pk) => {
            var url = this.getEventSourceUrl(pk)
            this.cal.fullCalendar('removeEventSource', url)
        })
    },
    mounted () {
        this.cal = $(this.$el)
        var args = {
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            defaultView: 'agendaWeek',
            locale: this.$language.current,
            timezone: 'local',
            selectable: true,
            selectHelper: true,
            editable: true,
            eventLimit: true,
            select: this.selectCallback,
            eventClick: this.eventClickCallback,
            eventDrop: this.eventDropCallback,
            eventResize: this.eventResizeCallback,
            themeSystem: 'bootstrap3'
        }
        this.cal.fullCalendar(args)
        this.addEventSources(this.calendars)
        this.addEventSources(this.sharedCalendars)
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
        getEventSourceUrl (calendarPk, type) {
            return '/api/v1/' + type + '-calendars/' + calendarPk + '/events/'
        },
        addEventSources (calendars) {
            var currentSources = this.cal.fullCalendar('getEventSources')
            for (var calendar of calendars) {
                var calType = (calendar.domain) ? 'shared' : 'user'
                var url = this.getEventSourceUrl(calendar.pk, calType)
                var present = false
                for (var source of currentSources) {
                    if (source.url === url) present = true
                }
                if (!present) {
                    this.cal.fullCalendar('addEventSource', url)
                }
            }
        },
        selectCallback (start, end) {
            this.start = new Date(start)
            this.end = new Date(end)
            this.allDay = !start.hasTime()
            this.showCreateEventForm = true
        },
        closeCreateEventForm () {
            this.showCreateEventForm = false
        },
        renderEvent (event) {
            this.cal.fullCalendar('renderEvent', event, true)
        },
        eventClickCallback (calEvent, jsEvent, view) {
            var calType = (calEvent.calendar.domain) ? 'shared' : 'user'
            this.$router.push({
                name: 'EditEvent',
                params: {
                    calendar_type: calType,
                    calendar_pk: calEvent.calendar.pk,
                    pk: calEvent.id
                }
            })
        },
        updateEventDates (calEvent) {
            var data = {
                start: calEvent.start,
                end: calEvent.end
            }
            if (calEvent.allDay) {
                var end = DateTime.fromISO(data.start.format())
                end.plus({days: 1})
                data.start.time('00:00:00')
                data.end = end
                data.allDay = calEvent.allDay
            }
            api.patchEvent(calEvent.calendar, calEvent.id, data).then(response => {
                this.$notify({
                    group: 'default',
                    title: this.$gettext('Success'),
                    type: 'success',
                    text: this.$gettext('Event updated')
                })
            })
        },
        eventDropCallback (calEvent) {
            this.updateEventDates(calEvent)
        },
        eventResizeCallback (calEvent) {
            this.updateEventDates(calEvent)
        },
        deleteEvent (id) {
            this.cal.fullCalendar('removeEvents', id)
        }
    }
}
</script>

<style src="fullcalendar/dist/fullcalendar.css"></style>
