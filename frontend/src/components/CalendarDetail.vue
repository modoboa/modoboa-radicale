<template>
  <modal>
    <div slot="header">
      <h3 class="modal-title"><translate>Calendar information</translate></h3>
    </div>
    <div slot="body">
      <p><translate>To access this calendar from the outside (such as Mozilla Thunderbird or your smartphone), use the following URL: </translate></p>
      <div class="alert alert-info">
        {{ calendar.url }}
      </div>
      <p><translate>The credentials are the same than the ones you use to access Modoboa.</translate></p>
      <hr>
      <div class="pull-right">
        <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
      </div>
      <div class="clearfix"></div>
    </div>
  </modal>
</template>

<script>
export default {
    props: {
        calendar: Object
    },
    methods: {
        close () {
            this.$emit('update:show', false)
        }
    }
}
</script>
