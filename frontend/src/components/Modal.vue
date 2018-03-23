<template>
  <div ref="modal" class="modal fade show in background-darken" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <slot name="header"></slot>
        </div>
        <div class="modal-body">
          <slot name="body"></slot>
        </div>
        <div v-if="showFooter" class="modal-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    props: {
        showFooter: {
            type: Boolean,
            default: false
        }
    }
}
</script>

<style scoped>
 .background-darken {
     background: rgba(0, 0, 0, 0.5);
     overflow-y: auto;
 }
</style>
