<template>
<modal>
  <div slot="header">
    <h3 class="modal-title"><translate>Import events</translate></h3>
  </div>
  <div slot="body">
    <form class="form-inline" v-on:submit.prevent="sendFile">
      <div class="alert alert-info">
        <translate>Select an ICS file to import and click on the Send button</translate>
      </div>
      <input type="file" name="file" ref="file" @change="setFile" />
      <span v-if="formErrors['ics_file']" class="help-block">{{ formErrors['ics_file'][0] }}</span>
      <hr>
      <div class="pull-right">
        <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
        <input type="submit" class="btn btn-primary" :disabled="runningUpload"
               :value="submitLabel">
      </div>
      <div class="clearfix"></div>
    </form>
  </div>
</modal>
</template>

<script>
import * as api from '@/api'

export default {
    props: {
        calendar: Object,
        show: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            file: null,
            formErrors: {},
            runningUpload: false
        }
    },
    computed: {
        submitLabel () {
            return this.$gettext('Send')
        }
    },
    methods: {
        close () {
            this.formErrors = {}
            this.$emit('update:show', false)
        },
        setFile () {
            this.file = this.$refs.file.files[0]
        },
        onSendError (response) {
            this.formErrors = response.data
            this.runningUpload = false
        },
        sendFile () {
            var data = new FormData()
            data.append('ics_file', this.file)
            this.runningUpload = true
            api.importEvents(this.calendar, data).then(response => {
                this.close()
                var msg = this.$ngettext(
                    '%{ n } event imported', '%{ n } events imported',
                    response.data.counter
                )
                this.$bus.$emit('eventsImported', this.calendar)
                this.$notify({
                    group: 'default',
                    title: this.$gettext('Success'),
                    type: 'success',
                    text: this.$gettextInterpolate(msg, { n: response.data.counter })
                })
            }, this.onSendError)
        }
    }
}
</script>
