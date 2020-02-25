<template>
  <div>
    <h3><translate>Edit event</translate></h3>
    <hr>

    <form id="eventForm" class="form-horizontal" method="post"
          v-on:submit.prevent="saveEvent"
          enctype="multipart/form-data">
      <div class="form-group" :class="{ 'has-error': formErrors['title'] || formErrors['title'] }">
        <div class="col-sm-10">
          <input v-model="event.title" type="text" id="title" name="title" class="form-control" :placeholder="titlePlaceHolder">
          <span v-if="formErrors['title']" class="help-block">{{ formErrors['title'][0] }}</span>
        </div>
      </div>
      <div class="form-group">
        <div class="col-sm-3">
          <flat-pickr name="start" v-model="event.start" :config="config"></flat-pickr>
        </div>
        <div class="col-sm-3">
          <flat-pickr name="end" v-model="event.end" :config="config"></flat-pickr>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-3">
          <div class="checkbox">
            <label><input type="checkbox" v-model="event.allDay"> <translate>All day</translate></label>
          </div>
        </div>
        <div class="col-sm-1">
          <span class="fa fa-calendar fa-2x"></span>
        </div>
        <div class="col-sm-6">
          <multiselect label="name" :options="allCalendars" v-model="event.calendar"></multiselect>
          <span v-if="formErrors['calendar']" class="help-block has-error">{{ formErrors['calendar'] }}</span>
        </div>
      </div>
      <hr>
      <div class="form-group" :class="{ 'has-error': formErrors['description'] || formErrors['description'] }">
        <div class="col-sm-7">
          <h4><translate>Detail</translate></h4>
          <textarea v-model="event.description" id="description" name="description" class="form-control" :placeholder="descriptionPlaceHolder"></textarea>
          <span v-if="formErrors['description']" class="help-block">{{ formErrors['description'][0] }}</span>
        </div>
        <div class="col-sm-5">
          <h4><translate>Attendees</translate></h4>
          <multiselect multiple label="display_name" :options="attendees"
                       v-model="event.attendees" :close-on-select="false"
                       :hide-selected="true" track-by="email">
          </multiselect>
        </div>
      </div>

      <hr>
      <div class="pull-right">
        <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
        <button type="button" class="btn btn-danger" @click="deleteEvent"><translate>Delete</translate></button>
        <input type="submit" class="btn btn-primary" :value="submitPlaceholder">
      </div>
      <div class="clearfix"></div>
    </form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'

export default {
    data () {
        return {
            event: {
                attendees: []
            },
            originalCalendarPk: null,
            formErrors: {},
            config: {
                enableTime: true,
                time_24hr: true
            }
        }
    },
    computed: {
        descriptionPlaceHolder () {
            return this.$gettext('Description')
        },
        titlePlaceHolder () {
            return this.$gettext('Title')
        },
        submitPlaceholder () {
            return this.$gettext('Save')
        },
        ...mapGetters([
            'calendars',
            'sharedCalendars',
            'attendees'
        ]),
        allCalendars () {
            return this.calendars.concat(this.sharedCalendars)
        }
    },
    mounted () {
        var params = this.$route.params
        api.getEvent(params.calendar_pk, params.calendar_type, params.pk).then(response => {
            this.event = response.data
        })
        this.$store.dispatch('getAttendees')
    },
    methods: {
        close () {
            this.formErrors = {}
            this.$router.push({ name: 'Calendar' })
        },
        onSaveError (response) {
            this.formErrors = response.data
        },
        saveEvent () {
            var event = JSON.parse(JSON.stringify(this.event))
            if (!event.calendar) {
                this.$set(this.formErrors, 'calendar', this.$gettext('A calendar is required.'))
                return
            }
            var originalCalendar = {
                pk: this.$route.params.calendar_pk,
                type: this.$route.params.calendar_type
            }
            api.updateEvent(originalCalendar, event.id, event).then(response => {
                this.close()
                this.$notify({
                    group: 'default',
                    title: this.$gettext('Success'),
                    type: 'success',
                    text: this.$gettext('Event updated')
                })
            }, this.onSaveError)
        },
        deleteEvent () {
            var msg = this.$gettext('Are you sure you want to remove this event?')
            this.$dialog.confirm(msg).then(() => {
                api.deleteEvent(this.event.calendar, this.event.id).then(response => {
                    this.close()
                    this.$notify({
                        group: 'default',
                        title: this.$gettext('Success'),
                        type: 'success',
                        text: this.$gettext('Event deleted')
                    })
                })
            })
        }
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
