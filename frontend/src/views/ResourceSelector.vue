<template>
  <div class="row justify-content-md-center">
    <div class="home col-md-6 justify-content-md-center">
      <VersionSelector/>
      <ResourcesList/>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import VersionSelector from "@/components/ResourceSelector/VersionSelector.vue";
import ResourcesList from "@/components/ResourceSelector/ResourcesList.vue";
import store from "@/store";

export default Vue.extend({
  name: 'ResourceSelector',
  components: {
    ResourcesList,
    VersionSelector,
  },
  data() {
    return {
      k8sVersion: store.state.k8sVersion
    }
  },
  mounted() {
    store.commit('selectResource', null)
    store.commit('disableImportButton', false);
  }
});
</script>
