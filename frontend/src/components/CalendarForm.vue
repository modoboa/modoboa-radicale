<template>
  <modal>
    <div slot="header">
      <h3 v-if="calendar.pk" class="modal-title"><translate>Edit calendar</translate></h3>
      <h3 v-else class="modal-title"><translate>New calendar</translate></h3>
    </div>

    <div slot="body">
      <form id="calendarForm" class="form-horizontal" method="post"
            v-on:submit.prevent="saveCalendar"
            enctype="multipart/form-data">
        <div class="form-group" :class="{ 'has-error': formErrors['name'] || formErrors['name'] }">
          <div class="col-sm-10">
            <input v-model="calendar.name" type="text" id="name" name="name" class="form-control" :placeholder="namePlaceHolder">
            <span v-if="formErrors['name']" class="help-block">{{ formErrors['name'][0] }}</span>
          </div>
        </div>
        <h4><small><translate>Color</translate></small></h4>
        <compact-picker v-model="calendar.color" />
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
import { Compact } from 'vue-color'
import Modal from './Modal.vue'

export default {
    props: {
        initialCalendar: {
            type: Object,
            default: () => { return { color: '' } }
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
            calendar: JSON.parse(JSON.stringify(this.initialCalendar)),
            formErrors: {}
        }
    },
    computed: {
        colorPlaceHolder () {
            return this.$gettext('Color')
        },
        namePlaceHolder () {
            return this.$gettext('Name')
        },
        submitLabel () {
            if (this.calendar.pk) {
                return this.$gettext('Update')
            }
            return this.$gettext('Create')
        }
    },
    methods: {
        close () {
            this.$emit('update:show', false)
        },
        saveCalendar () {
            var action
            var msg
            var data = JSON.parse(JSON.stringify(this.calendar))

            data.color = data.color.hex
            if (this.calendar.pk) {
                action = 'updateCalendar'
                msg = this.$gettext('Calendar updated')
            } else {
                action = 'createCalendar'
                msg = this.$gettext('Calendar created')
            }
            this.$store.dispatch(action, data).then(() => {
                if (data.color !== this.initialCalendar.color) {
                    this.$bus.$emit('calendarColorChanged', data)
                }
                this.close()
                this.$notify({
                    group: 'default',
                    title: this.$gettext('Success'),
                    type: 'success',
                    text: msg
                })
            })
        }
    }
}
</script>
