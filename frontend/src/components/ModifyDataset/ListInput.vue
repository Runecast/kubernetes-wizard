<template>
<div>
  <span class="text-primary">Value</span>
  <div class="input-group" v-for="(index, key) in indices" :key="key">
    <input
      ref="input"
      v-model="value[index]"
      :id="`value-${index}`"
      class="form-control"
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
        id="add-button"
        :disabled="disableAddButton"
        @click="incrementIndicesList()"
    >
      Add
    </button>
  </div>
</div>
</template>

<script>
export default {
  name: "ListInput",
  data() {
    return {
      indices: [0],
      value: {},
    }
  },
  computed: {
    disableAddButton() {
      let disable = false;
      this.indices.forEach((index) => {
        if (!this.value[index]) {
          disable = true;
        }
      })
      return disable
    },
  },
  mounted() {
    console.log(this.$root)
    console.log(this.$root.$children[0])
    console.log(this.$root.$children[0].$children[1].$refs['modification-form'])

  },
  methods: {
    incrementIndicesList() {
      let max = Math.max(...this.indices);
      this.indices.push(max+1);
      this.$mount();
    },
    removeListItem(index) {
      this.value[index] = undefined;
      this.indices.splice(this.indices.indexOf(index), 1);
      this.$mount();
      // this.$root.$children[0].$children[1].$refs['modification-form'].updateValues();
        this.$root.$children[0].$children[1].$refs['modification-form'].updateValues()
    },
    setValueOfLastInput(value) {
      let lastIndex = this.indices[this.indices.length-1]
      this.value[lastIndex] = value
      this.$mount();
    },
  },
}
</script>

<style scoped>

</style>