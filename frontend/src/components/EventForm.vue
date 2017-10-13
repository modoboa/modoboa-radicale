<template>
  <modal>
    <div slot="header">
      <h3 class="modal-title"><translate>Edit event</translate></h3>
    </div>

    <div slot="body">
      <form id="eventForm" class="form-horizontal" method="post"
            v-on:submit.prevent="saveEvent"
            enctype="multipart/form-data">
        <div class="form-group" :class="{ 'has-error': formErrors['title'] || formErrors['title'] }">
          <div class="col-sm-10">
            <input v-model="event.title" type="text" id="title" name="title" class="form-control" :placeholder="titlePlaceHolder">
            <span v-if="formErrors['title']" class="help-block">{{ formErrors['title'][0] }}</span>
          </div>
        </div>
        {{ event.start|formatDate }} - {{ event.end|formatDate }}
        <div class="form-group" :class="{ 'has-error': formErrors['description'] || formErrors['description'] }">
          <div class="col-sm-7">
            <h4><translate>Detail</translate></h4>
            <textarea v-model="event.description" id="description" name="description" class="form-control" :placeholder="descriptionPlaceHolder"></textarea>
            <span v-if="formErrors['description']" class="help-block">{{ formErrors['description'][0] }}</span>
          </div>
          <div class="col-sm-5">
            <h4><translate>Attendees</translate></h4>
            
          </div>
        </div>

        <hr>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
          <button type="button" class="btn btn-danger" @click="deleteEvent"><translate>Delete</translate></button>          
          <input type="submit" class="btn btn-primary" value="Save">
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </modal>
</template>

<script>
 import Modal from './Modal.vue'
 import * as api from '../api'

 export default {
     components: {
         'modal': Modal
     },
     props: {
         id: [String],
         show: {
             type: Boolean,
             default: false
         }
     },
     data () {
         return {
             event: {},
             formErrors: {}
         }
     },
     computed: {
         descriptionPlaceHolder () {
             return this.$gettext('Description')
         },
         titlePlaceHolder () {
             return this.$gettext('Title')
         }
     },
     mounted () {
         api.getEvent(this.id).then(response => {
             this.event = response.data
         })
     },
     methods: {
         close () {
             this.$emit('update:show', false)
         },
         saveEvent () {
             var event = {
                 title: this.event.title,
                 start: this.start,
                 end: this.end
             }
             api.updateEvent(this.event.id, event).then(response => {
                 this.close()
                 this.$emit('eventCreated', response.data)
             })
         },
         deleteEvent () {
             api.deleteEvent(this.event.id).then(response => {
                 this.close()
                 this.$emit('eventDeleted', this.event.id)
             })
         }
     }
 }
</script>
