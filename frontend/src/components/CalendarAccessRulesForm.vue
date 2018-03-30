<template>
  <modal>
    <div slot="header">
      <h3 class="modal-title"><translate>Calendar sharing</translate></h3>
    </div>

    <div slot="body">
      <form id="accessRulesForm" class="form-inline" method="post">
        <div class="row">
          <div class="col-sm-6">
            <multiselect label="full_address" :options="mailboxes" v-model="currentRule.mailbox"></multiselect>
            <span v-if="formErrors['mailbox']" class="help-block">{{ formErrors['mailbox'][0] }}</span>
          </div>
          <div class="col-sm-4">
            <label class="checkbox"><input type="checkbox" v-model="currentRule.read"> <translate>Read</translate></label>
            <label class="checkbox"><input type="checkbox" v-model="currentRule.write"> <translate>Write</translate></label>
          </div>
          <div class="col-sm-2">
            <a class="btn btn-primary" href="#" @click="saveRule"><span class="fa fa-save"></span></a>
          </div>
        </div>
      </form>
      <br>
      <table class="table">
        <thead>
          <tr>
            <th><translate>Account</translate></th>
            <th><translate>Read</translate></th>
            <th><translate>Write</translate></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rule in accessRules" :key="rule.pk">
            <td>{{ rule.mailbox.full_address }}</td>
            <td>
              <span v-if="rule.read" class="fa fa-check"></span>
              <span v-else class="fa fa-close"></span>
            </td>
            <td>
              <span v-if="rule.write" class="fa fa-check"></span>
              <span v-else class="fa fa-close"></span>
            </td>
            <td>
              <a href="#" @click="editRule(rule)"><span class="fa fa-edit"></span></a>
              <a href="#" @click="deleteRule(rule.pk)"><span class="fa fa-trash"></span></a>
            </td>
          </tr>
        </tbody>
      </table>
      <hr>
      <div class="pull-right">
        <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
      </div>
      <div class="clearfix"></div>
    </div>
  </modal>
</template>

<script>
import Vue from 'vue'
import * as api from '@/api'

export default {
    props: {
        calendarPk: Number
    },
    data () {
        return {
            accessRules: [],
            mailboxes: [],
            currentRule: {},
            formErrors: {}
        }
    },
    created () {
        api.getAccessRules(this.calendarPk).then(response => {
            this.accessRules = response.data
            if (!this.accessRules.length) {
                this.accessRules = []
            }
        })
        api.getMailboxes().then(response => {
            this.mailboxes = response.data
        })
    },
    methods: {
        saveRule () {
            if (!this.currentRule.pk) {
                this.currentRule.calendar = this.calendarPk
                api.createAccessRule(this.currentRule).then(response => {
                    this.accessRules.push(response.data)
                    this.resetForm()
                }, this.onError)
            } else {
                api.updateAccessRule(this.currentRule.pk, this.currentRule).then(response => {
                    this.accessRules.filter((item, pos) => {
                        if (item.pk === this.currentRule.pk) {
                            Vue.set(this.accessRules, pos, this.currentRule)
                        }
                    })
                    this.resetForm()
                }, this.onError)
            }
        },
        resetForm () {
            this.currentRule = {}
            this.formErrors = {}
        },
        onError (response) {
            this.formErrors = response.data
        },
        editRule (rule) {
            this.currentRule = JSON.parse(JSON.stringify(rule))
        },
        deleteRule (pk) {
            api.deleteAccessRule(pk).then(response => {
                this.accessRules = this.accessRules.filter(function (rule) {
                    return rule.pk !== pk
                })
            })
        },
        close () {
            this.formErrors = {}
            this.$emit('update:show', false)
        }
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
