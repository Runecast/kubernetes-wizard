<template>
<div class="btn-group float-end" role="group" aria-label="YAML output buttons">
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

export default {
  name: "CopyButton",
  methods: {
    copyYamlToClipboard() {
      let outputYaml = store.state.parsedModifications;
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