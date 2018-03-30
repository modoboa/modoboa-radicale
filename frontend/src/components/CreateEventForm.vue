<template>
  <modal>
    <div slot="header">
      <h3 class="modal-title"><translate>New event</translate></h3>
    </div>

    <div slot="body">
      <form id="eventForm" class="form-horizontal" method="post"
            v-on:submit.prevent="saveEvent"
            enctype="multipart/form-data">
        <div class="form-group" :class="{ 'has-error': formErrors['title'] || formErrors['title'] }">
          <div class="col-sm-offset-2 col-sm-10">
            <input v-model="event.title" type="text" id="title" name="title" class="form-control" :placeholder="titlePlaceHolder">
            <span v-if="formErrors['title']" class="help-block">{{ formErrors['title'][0] }}</span>
          </div>
        </div>
        <div class="form-group">
          <div class="col-sm-2"><span class="fa fa-clock-o fa-2x"></span></div>
          <div class="col-sm-5">
            <flat-pickr name="start" v-model="event.start" :config="config"></flat-pickr>
          </div>
          <div class="col-sm-5">
            <flat-pickr name="end" v-model="event.end" :config="config"></flat-pickr>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2"><span class="fa fa-calendar fa-2x"></span></div>
          <div class="col-sm-10">
            <multiselect label="name" :options="allCalendars" v-model="event.calendar"></multiselect>
            <span v-if="formErrors['calendar']" class="help-block">{{ formErrors['calendar'] }}</span>
          </div>
        </div>
        <hr>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
          <input type="submit" class="btn btn-primary" :value="submitLabel">
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </modal>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'

export default {
    props: {
        start: [Date],
        end: [Date],
        allDay: {
            type: Boolean,
            default: false
        },
        show: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            event: {
                start: this.start,
                end: this.end,
                allDay: this.allDay
            },
            formErrors: {},
            config: {
                enableTime: true,
                time_24hr: true
            }
        }
    },
    computed: {
        titlePlaceHolder () {
            return this.$gettext('Title')
        },
        submitLabel () {
            return this.$gettext('Save')
        },
        ...mapGetters([
            'calendars',
            'sharedCalendars'
        ]),
        allCalendars () {
            return this.calendars.concat(this.sharedCalendars)
        }
    },
    methods: {
        close () {
            this.formErrors = {}
            this.$emit('update:show', false)
        },
        saveEvent () {
            var event = JSON.parse(JSON.stringify(this.event))
            if (!event.calendar) {
                this.$set(this.formErrors, 'calendar', this.$gettext('A calendar is required.'))
                return
            }
            var calendar = event.calendar
            event.calendar = event.calendar.pk
            api.createEvent(calendar, event).then(response => {
                this.close()
                this.$emit('eventCreated', response.data)
            })
        }
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
