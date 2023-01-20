<template>
<div>
  <label class="form-label">
    <span class="text-primary">{{ name[0].toUpperCase() + name.substring(1) }}</span>
  </label>
  <select
      :id="name"
    class="form-control"
  >
    <option></option>
    <option
      v-for="(value, key) in values"
      :key="key"
      :value="value"
      >
      {{ value }}
    </option>
  </select>
</div>
</template>

<script>
export default {
  name: "SelectField",
  props: ['values', 'name']
}
</script>

<style scoped>

</style>