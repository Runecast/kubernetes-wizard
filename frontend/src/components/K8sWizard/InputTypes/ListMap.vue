<template>
<div class="mt-3">
  <div class="accordion" :id="`accordion-map-${getIdFromPath}`">
    <div class="accordion-item" v-for="keyIndex in keyIndices" :key="keyIndex">
      <h2 class="accordion-header" :id="`heading-map-${getNumberedIdFromPath(keyIndex)}`">
        <div
            class="btn-group w-100"
            role="group"
            aria-label="Header button group"
        >
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            aria-expanded="false"
            :data-bs-target="`#collapse-map-${getNumberedIdFromPath(keyIndex)}`"
            :aria-controls="`collapse-map-${getNumberedIdFromPath(keyIndex)}`"
          >
            <span class="text-primary">{{ parameterName }}</span>&nbsp;<span v-if="parameterData['required']" class="text-secondary">(required)</span>
          </button>
          <a
            v-if="keyIndices.length > 1"
            @click="removeListItem(keyIndex)"
            type="button"
            class="close text-muted btn-light-grey button-close disabled"
            aria-label="Close"
          >
            <span class="p-3 button-close-icon">&times;</span>
          </a>
        </div>
      </h2>
      <div
        class="accordion-collapse collapse"
        :id="`collapse-map-${getNumberedIdFromPath(keyIndex)}`"
        :aria-labelledby="`heading-map-${getNumberedIdFromPath(keyIndex)}`"
        :data-bs-parent="`#accordion-map-${getIdFromPath}`"
      >
        <div class="accordion-body">
          <div v-if="parameterData['description']" v-html="`${parameterData['description']}<hr>`"></div>
            <label class="form-label">
              <span class="text-primary">Key</span>
            </label>
            <input
              ref="key"
              :id="getKeyIdFromPath"
              v-model="keys[keyIndex]"
              class="form-control"
            />
            <label class="form-label">
              <span class="text-primary">Values</span>
            </label>
            <div class="input-group" v-for="valueIndex in valueIndices[keyIndex]" :key="valueIndex">
              <input
                :key="valueIndex"
                :id="getValueNumberedIdFromPath(keyIndex, valueIndex)"
                :placeholder="defaultValue"
                :data-bs-content="description"
                class="form-control"
                data-bs-toggle="popover"
                data-bs-trigger="focus"
              />
              <button
                class="input-group-text"
                type="button"
                v-if="valueIndices[keyIndex].length > 1"
                @click="removeValueListItem(keyIndex, valueIndex)"
              >×</button>

            </div>
          <div class="text-center mt-1">
            <button
                class="btn btn-outline-primary"
                type="button"
                :id="`add-button-m${keyIndex}`"
                @click="incrementValueIndicesList(keyIndex)"
            >
              Add
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="text-center mt-1">
    <button
        class="btn btn-outline-primary"
        type="button"
        :id="`add-button-${getIdFromPath}`"
        @click="incrementIndicesList()"
    >
      Add
    </button>
  </div>
</div>
</template>

<script>
export default {
  name: "ListMap",
  props: ['parameterData', 'parameterName', 'idPath'],
  data() {
    return {
      keyIndices: [0], // Indices of the key-value pairs in the map
      valueIndices: {0: [0]},  // Indices of the elements in the values of the map
      keys: {},  // Name given to the key of each element of the map
    }
  },
  computed: {
    getIdFromPath() {
      return [...this.idPath, this.parameterName].join('-')
    },
    getKeyIdFromPath() {
      let fullIdPath = [...this.idPath, this.parameterName];
      return ['LISTMAPKEY'].concat(fullIdPath).join('-');
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
  methods: {
    incrementIndicesList() {
      let max = Math.max(...this.keyIndices);
      this.keyIndices.push(max + 1);
      this.valueIndices[max + 1] = [0];
    },
    removeListItem(keyIndex) {
      this.keyIndices.splice(this.keyIndices.indexOf(keyIndex), 1);
      delete this.valueIndices[keyIndex];
      this.$mount();
      this.$root.$children[0].$children[1].$refs['parameter-browser'].updateUserInput();
    },
    incrementValueIndicesList(keyIndex) {
      let max = Math.max(...this.valueIndices[keyIndex]);
      this.valueIndices[keyIndex].push(max+1);
      this.$forceUpdate();
    },
    removeValueListItem(keyIndex, valueIndex) {
      this.valueIndices[keyIndex].splice(this.valueIndices[keyIndex].indexOf(valueIndex), 1);
      this.$mount();
      this.$root.$children[0].$children[1].$refs['parameter-browser'].updateUserInput();
    },
    getNumberedIdFromPath(keyIndex) {
      return [...this.idPath, `m${keyIndex}`, this.parameterName].join('-')
    },
    getValueNumberedIdFromPath(keyIndex, valueIndex) {
      return [...this.idPath, `m${keyIndex}`, this.keys[keyIndex], valueIndex].join('-')
    },
  },
}
</script>

<style scoped>

</style>