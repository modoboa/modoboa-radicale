<template>
  <modal>
    <div slot="header">
      <h3 v-if="pk" class="modal-title"><translate>Edit calendar</translate></h3>
      <h3 v-else class="modal-title"><translate>New calendar</translate></h3>
    </div>

    <div slot="body">
      <form id="calendarForm" class="form-horizontal" method="post"
            v-on:submit.prevent="createCalendar"
            enctype="multipart/form-data">
        <div class="form-group" :class="{ 'has-error': formErrors['name'] || formErrors['name'] }">
          <div class="col-sm-10">
            <input v-model="calendar.name" type="text" id="name" name="name" class="form-control" :placeholder="namePlaceHolder">
            <span v-if="formErrors['name']" class="help-block">{{ formErrors['name'][0] }}</span>
          </div>
        </div>
        <h4><small><translate>Color</translate></small></h4>
        <compact-picker :value="colors" :presetColors="colors" @input="updateColor" />
        <hr>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
          <input type="submit" class="btn btn-primary" value="Create">
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </modal>
</template>

<script>
 import { Compact } from 'vue-color'
 import Modal from './Modal.vue'
 import * as api from '../api'

 export default {
     props: {
         pk: {
             type: Number,
             default: null
         },
         show: {
             type: Boolean,
             default: false
         }
     },
     components: {
         'compact-picker': Compact,
         'modal': Modal
     },
     data () {
         return {
             calendar: {},
             colors: {
                 hex: null
             },
             formErrors: {}
         }
     },
     computed: {
         colorPlaceHolder () {
             return this.$gettext('Color')
         },
         namePlaceHolder () {
             return this.$gettext('Name')
         }
     },
     created () {
         if (!this.pk) {
             return
         }
         api.getUserCalendar(this.pk).then(response => {
             this.calendar = response.data
             this.colors.hex = response.data.color
         })
     },
     methods: {
         close () {
             this.$emit('update:show', false)
         },
         updateColor (value) {
             this.calendar.color = value.hex
         },
         createCalendar () {
             api.createUserCalendar(this.calendar).then(response => {
                 this.close()
             })
         }
     }
 }
</script>
