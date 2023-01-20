<template>
<div>
    <label class="form-label">
      <span class="text-primary">
        {{ parameterName }}</span>
      <span v-if="required" class="text-secondary">&nbsp;(required)</span>
    </label>
    <div class="input-group" v-for="(index, key) in indices" :key="key">
      <input
        ref="input"
        v-model="value[index]"
        :id="getIdFromPath(index)"
        :placeholder="defaultValue"
        :data-bs-content="description"
        class="form-control"
        data-bs-toggle="popover"
        data-bs-trigger="focus"
        value=""
      />
      <button
        class="input-group-text"
        type="button"
        v-if="indices.length > 1"
        @click="removeListItem(index)"
      >×</button>
    </div>
    <div class="text-center mt-1">
      <button
          class="btn btn-outline-primary"
          type="button"
          :id="`add-button-${getAddButtonIdFromPath()}`"
          :disabled="disableAddButton"
          @click="incrementIndicesList()"
      >
        Add
      </button>
    </div>
</div>
</template>

<script>
import bootstrap from "/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"

export default {
  name: "SimpleInputList",
  props: ['parameterData', 'parameterName', 'idPath', 'addButtonIndex'],
  data() {
    return {
      indices: [0],
      value: {},
    }
  },
  computed: {
    disableAddButton() {
      let disable = false;
      this.indices.forEach( (index) => {
        if (!this.value[index]) {
          disable = true;
        }
      })
      return disable
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
    // Enable popovers
    let inputs = this.$refs['input']
    return [...inputs].map(input => new bootstrap.Popover(input, {html: true}));
  },
  methods: {
    incrementIndicesList() {
      let max = Math.max(...this.indices);
      this.indices.push(max+1);
      this.$mount();
      let inputs = this.$refs['input'].slice(-1)
      return [...inputs].map(input => new bootstrap.Popover(input, {html: true}));
    },
    removeListItem(index) {
      this.value[index] = undefined;
      this.indices.splice(this.indices.indexOf(index), 1);
      this.$mount();
      this.$root.$children[0].$children[1].$refs['parameter-browser'].updateUserInput();
    },
    setValueOfLastInput(value) {
      let lastIndex = this.indices[this.indices.length-1]
      this.value[lastIndex] = value
      this.$mount();
    },
    getIdFromPath(index) {
      return this.idPath.concat(index).join('-')
    },
    getAddButtonIdFromPath() {
      return this.idPath.join('-')
    },
  },
}
</script>

<style scoped>

</style>