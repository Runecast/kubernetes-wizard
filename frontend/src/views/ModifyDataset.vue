<template>
<div class="row">
  <div id="left-panel" class="col-md-6 overflow-auto">
    <ModificationForm ref="modification-form"/>
  </div>
  <div id="result-wrapper" class="col-md-6 overflow-auto">
    <OutputWrapper/>
  </div>
</div>
</template>

<script>
import Vue from 'vue';
import ModificationForm from "@/components/ModifyDataset/ModificationForm";
import OutputWrapper from "@/components/ModifyDataset/OutputWrapper";

export default Vue.extend({
  name: "ModifyDataset",
  components: {
    ModificationForm,
    OutputWrapper
  },
});
</script>

<style scoped>

</style>