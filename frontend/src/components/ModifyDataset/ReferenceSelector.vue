<template>
<div>
  <label class="form-label">
    <span class="text-primary">{{ name[0].toUpperCase() + name.substring(1) }}</span>
  </label>
  <input
    :id="name"
    list="references-list"
    class="form-control"
  />
  <datalist
    id="references-list"
    style="width:100%"
  >
    <option
      v-for="(value, key) in list"
      :key="key"
      :value="value"
      >
      {{ displayParameter(value) }}
    </option>
  </datalist>
</div>
</template>

<script>

export default {
  name: "ReferenceSelector",
  props: ['list', 'name'],
  methods: {
    displayParameter(value) {
      let split = value.split('.')
      let display = split.slice(-2).join('.') + ' (' + split[0].replace('-resources', '') + ')'
      display = display.startsWith('param')? display.slice(5): display
      return display
    }
  }
}

</script>

<style scoped>

</style>