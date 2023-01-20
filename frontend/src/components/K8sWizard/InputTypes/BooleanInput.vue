<template>
<div>
  <label class="form-label">
    <span class="text-primary">{{ parameterName }}</span>
    <span v-if="required" class="text-secondary">&nbsp;(required)</span>
  </label>
  <select
    ref="input"
    :id="getIdFromPath"
    :data-bs-content="description"
    class="form-control"
    aria-label="Boolean"
    data-bs-toggle="popover"
    data-bs-trigger="focus"
  >
    <option selected></option>
    <option v-if="defaultsToTrue" value="true">True (default)</option>
    <option v-else value="true">True</option>
    <option v-if="defaultsToFalse" value="false">False (default)</option>
    <option v-else value="false">False</option>
  </select>
</div>
</template>

<script>
import bootstrap from "/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"

export default {
  name: "BooleanInput",
  props: ['parameterData', 'parameterName', 'idPath'],
  computed: {
    getIdFromPath() {
      return this.idPath.join('-')
    },
    defaultValue() {
      return this.parameterData['default']? this.parameterData['default']: '';
    },
    defaultsToTrue() {
      return String(this.defaultValue) === 'true';
    },
    defaultsToFalse() {
      return String(this.defaultValue) === 'false';
    },
    required() {
      return this.parameterData['required']? this.parameterData['required']: '';
    },
    description() {
      return this.parameterData['description']? this.parameterData['description'].replaceAll(/(https?:\/\/[\w\-_./#?]+)/g, '<a href="$1" target="_blank">$1</a>'): '';
    },
  },
  mounted() {
    // Set predefined value
    this.$refs['input'].value = this.parameterData['predefined_value'] ? this.parameterData['predefined_value'] : '';
    // Enable popovers
    return new bootstrap.Popover(this.$refs['input'], {html: true})
  },
  methods: {
    setInputValue(value) {
      this.$refs.input.value = value
    },
  }
}
</script>

<style scoped>

</style>