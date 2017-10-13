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
          <div class="col-sm-10">
            <input v-model="event.title" type="text" id="title" name="title" class="form-control" :placeholder="titlePlaceHolder">
            <span v-if="formErrors['title']" class="help-block">{{ formErrors['title'][0] }}</span>
          </div>
        </div>
        <h4>Date</h4>
        {{ start|formatDate }} - {{ end|formatDate }}
        <hr>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
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
         start: [Date],
         end: [Date],
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
         titlePlaceHolder () {
             return this.$gettext('Title')
         }
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
             api.createEvent(event).then(response => {
                 this.close()
                 this.$emit('eventCreated', response.data)
             })
         }
     }
 }
</script>
