<template>
<div class="mt-3">
  <div class="accordion" :id="`accordion-map-${getIdFromPath}`">
    <div class="accordion-item" v-for="index in indices" :key="index">
      <h2 class="accordion-header" :id="`heading-map-${getNumberedIdFromPath(index)}`">
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
            :data-bs-target="`#collapse-map-${getNumberedIdFromPath(index)}`"
            :aria-controls="`collapse-map-${getNumberedIdFromPath(index)}`"
          >
            <span class="text-primary">{{ parameterName }}</span>&nbsp;<span v-if="parameterData['required']" class="text-secondary">(required)</span>
          </button>
          <a
            v-if="indices.length > 1"
            @click="removeListItem(index)"
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
        :id="`collapse-map-${getNumberedIdFromPath(index)}`"
        :aria-labelledby="`heading-map-${getNumberedIdFromPath(index)}`"
        :data-bs-parent="`#accordion-map-${getIdFromPath}`"
      >
        <div class="accordion-body">
          <div v-if="parameterData['description']" v-html="`${parameterData['description']}<hr>`"></div>
            <label class="form-label">
              <span class="text-primary">Key</span>
            </label>
            <input
              ref="key"
              :id="getKeyIdFromPath(index)"
              class="form-control"
            />
            <label class="form-label">
              <span class="text-primary">Value</span>
            </label>
            <input
              ref="input"
              :id="getIdFromPath"
              :placeholder="defaultValue"
              :data-bs-content="description"
              class="form-control"
              data-bs-toggle="popover"
              data-bs-trigger="focus"
              :data-type="parameterData.type"
            />
        </div>
      </div>
    </div>
  </div>
  <div class="text-center mt-1">
    <button
        class="btn btn-outline-primary"
        type="button"
        :id="`add-button-${getIdFromPath}`"
        :ref="`ref-${getIdFromPath}`"
        @click="incrementIndicesList()"
    >
      Add
    </button>
  </div>
</div>
</template>

<script>
export default {
  name: "SimpleMap",
  props: ['parameterData', 'parameterName', 'idPath'],
  data() {
    return {
      indices: [0],  // Indices of the key-value pairs in the map
    }
  },
  computed: {
    getIdFromPath() {
      return [...this.idPath, this.parameterName].join('-')
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
    getKeyIdFromPath(keyIndex) {
      let fullIdPath = [...this.idPath, keyIndex];
      return ['MAPKEY'].concat(fullIdPath).join('-');
    },
    incrementIndicesList() {
      let max = Math.max(...this.indices);
      this.indices.push(max + 1);
      this.$mount();
    },
    removeListItem(index) {
      this.indices.splice(this.indices.indexOf(index), 1);
      this.$mount();
    },
    getNumberedIdFromPath(index) {
      return [...this.idPath, `m${index}`, this.parameterName].join('-')
    },
    setKey(key, index) {
      this.$refs.key[index].value = key;
      this.$mount();
      this.$forceUpdate();
    },
    setValue(value, index) {
      this.$refs.input[index].value = value;
      this.$mount();
      this.$forceUpdate();
    }
  },
}
</script>

<style scoped>

</style>