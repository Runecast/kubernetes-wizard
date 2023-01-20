<template>
  <div id="version-selector" :key="k8sVersion">
    <h2 class="mb-3 display-6 text-center">Versions</h2>
    <select id="select-version" class="form-select" @change="changeVersion($event)">
      <option
          :id="versions.latest"
          value="latest"
          :key="versions.latest"
          :selected="versions.latest === k8sVersion"
      >
        {{ versions.latest.replace('-', '.') }} (latest)
      </option>
      <option
        v-for="version in versions.old"
        :id="version"
        :value="version"
        :key="version"
        :selected="version === k8sVersion"
      >
        {{ version.replace('-', '.') }}
      </option>
    </select>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import store from '@/store/index'
import k8sVersions from '../../../config/k8s.json'

export default Vue.extend({
  name: "VersionSelector",
  data() {
    return {
      versions: k8sVersions,
      k8sVersion: store.state.k8sVersion
    }
  },
  computed: {
    displayVersion() {
      return store.getters.displayVersion
    }
  },
  methods: {
    changeVersion(event: Event) {
      store.commit('changeVersion', (event.target as HTMLInputElement).value);
    }
  }
})
</script>

<style scoped>

</style>