<template>
<div>
  <label class="form-label">
    <span class="text-primary">{{ parameterName }}</span>
    <span v-if="required" class="text-secondary">&nbsp;(required)</span>
  </label>
  <input
    ref="input"
    :id="getIdFromPath"
    :placeholder="defaultValue"
    :data-bs-content="description"
    class="form-control"
    data-bs-toggle="popover"
    data-bs-trigger="focus"
    :list="`datalist-${getIdFromPath}`"
  />
  <datalist
    :id="`datalist-${getIdFromPath}`"
  >
    <option v-for="(option, index) in options" :key="index" :value="option"></option>
  </datalist>
</div>
</template>

<script>
import bootstrap from "/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"

export default {
  name: "OptionsInput",
  props: ['parameterData', 'parameterName', 'idPath', 'options'],
  computed: {
    getIdFromPath() {
      return this.idPath.join('-')
    },
    defaultValue() {
      return this.parameterData['default']? this.parameterData['default']: '';
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
  }}
</script>

<style scoped>

</style>