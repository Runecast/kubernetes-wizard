<template>
<div class="btn-group float-end" role="group" aria-label="YAML output buttons">
  <button
    id="import-button"
    class="btn btn-outline-secondary"
    data-bs-toggle="modal"
    data-bs-target="#import-modal"
    :disabled="importDisabled"
  >
    Import
  </button>
  <button
    id="copy-button"
    class="btn btn-outline-secondary"
    @click="copyYamlToClipboard()"
  >
    Copy
  </button>
</div>
</template>

<script>
import store from "@/store";
import k8sVersions from "../../../config/k8s.json";

export default {
  name: "ActionButtons",
  data() {
    return {
      versions: k8sVersions,
    }
  },
  computed: {
    importDisabled() {
      return store.state.importButtonDisabled
    }
  },
  methods: {
    copyYamlToClipboard() {
      let outputYaml = store.state.parsedData;
      navigator.clipboard.writeText(outputYaml)
      .catch(err => {
        console.log('Couldn\'t copy to clipboard: ', err);
      });
    },
  }
}
</script>

<style scoped>

</style>