<template>
  <div>
    <create-event-form :start="start" :end="end" v-if="showCreateEventForm" :show.sync="showCreateEventForm" @eventCreated="renderEvent"></create-event-form>
    <event-form v-if="showEventForm" :id="currentId" :show.sync="showEventForm" @eventDeleted="deleteEvent"></event-form>
  </div>
</template>

<script>
 import $ from 'jquery'
 import fullCalendar from 'fullcalendar' // eslint-disable-line no-unused-vars
 import CreateEventForm from './CreateEventForm.vue'
 import EventForm from './EventForm.vue'

 export default {
     components: {
         'create-event-form': CreateEventForm,
         'event-form': EventForm
     },
     data () {
         return {
             currentId: null,
             start: null,
             end: null,
             showCreateEventForm: false,
             showEventForm: false
         }
     },
     props: {
         eventSources: {
             type: Array,
             required: true
         },
         locale: {
             type: String,
             default: 'en'
         }
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
             locale: this.locale,
             timezone: 'local',
             selectable: true,
             selectHelper: true,
             editable: true,
             eventLimit: true,
             eventSources: this.eventSources,
             select: this.selectCallback,
             eventClick: this.eventClickCallback
         }
         this.cal.fullCalendar(args)
     },
     methods: {
         selectCallback (start, end) {
             this.showCreateEventForm = true
             this.start = new Date(start)
             this.end = new Date(end)
         },
         closeCreateEventForm () {
             this.showCreateEventForm = false
         },
         renderEvent (event) {
             this.cal.fullCalendar('renderEvent', event, true)
         },
         eventClickCallback (calEvent, jsEvent, view) {
             this.currentId = calEvent.id
             this.showEventForm = true
         },
         deleteEvent (id) {
             this.cal.fullCalendar('removeEvents', id)
         }
     }
 }
</script>

<style src="fullcalendar/dist/fullcalendar.css"></style>
