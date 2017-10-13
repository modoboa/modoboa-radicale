<template>
  <modal>
    <div slot="header">
      <h3 class="modal-title"><translate>Calendar sharing</translate></h3>
    </div>

    <div slot="body">
      <form id="accessRulesForm" method="post" v-on:submit.prevent="applyRules">

        <accessrule-field v-for="(rule, index) in accessRules" :rule="rule" :key="index" :index="index" @add="addAccessRuleField" @delete="(index) => deleteAccessRule(index)"></accessrule-field>

        <hr>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
          <input type="submit" class="btn btn-primary" value="Apply">
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </modal>
</template>

<script>
 import AccessRuleField from './AccessRuleField.vue'
 import Modal from './Modal.vue'

 export default {
     components: {
         'accessrule-field': AccessRuleField,
         'modal': Modal
     },
     data () {
         return {
             accessRules: [{}]
         }
     },
     methods: {
         addAccessRuleField () {
             this.accessRules.push({})
         },
         applyRules () {

         },
         deleteAccessRule (index) {
             this.accessRules.splice(index, 1)
         },
         close () {
             this.$emit('update:show', false)
         }
     }
 }
</script>
