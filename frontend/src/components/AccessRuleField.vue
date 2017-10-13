<template>
  <div class="form-inline access-rule">
    <div class="row">
      <div class="col-sm-7">
        <input id="username" name="username" v-model="rule.username" class="form-control">
      </div>
      <div class="col-sm-3">
        <label class="checkbox"><input type="checkbox" v-model="rule.readaccess" id="readaccess" name="readaccess"> <translate>Read</translate></label>
        <label class="checkbox"><input type="checkbox" v-model="rule.writeaccess" id="writeaccess" name="writeaccess"> <translate>Write</translate></label>
      </div>
      <div class="col-sm-2">
        <a href="#" class="addrule" v-on:click.prevent="$emit('add')"><span class="fa fa-plus"></span></a>
        <a v-if="index" href="#" v-on:click.prevent="$emit('delete', index)"><span class="fa fa-trash"></span></a>
      </div>
    </div>
  </div>
</template>

<script>
 export default {
     props: {
         rule: Object,
         index: {
             type: Number,
             required: true
         }
     }
 }
</script>

<style>
 .access-rule {
     margin-top: 5px;
 }
 .addrule {
     margin-left: 10px;
 }

</style>
