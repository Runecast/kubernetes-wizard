<template>
<div class="modal fade" id="import-modal" tabindex="-1" aria-labelledby="import-modal-label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="import-modal-label">Import YAML</h2>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <form id="import-form">
        <div class="modal-body">
          <label for="import-textarea">Paste below the YAML to import</label>
          <textarea
            class="form-control"
            id="import-textarea"
            spellcheck="false"
            rows="20"
            ref="yamlInput"
          ></textarea>
        </div>
        <div class="modal-footer">
          <span id="import-error" class="text-danger fst-italic"></span>
          <button
            id="submit-import-button"
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="parseYaml()"
          >Submit</button>
        </div>
      </form>
    </div>
  </div>
</div>

</template>

<script>
import jsyaml from "@/js-yaml.min"
import store from "@/store";

export default {
  name: "ImportModal",
  data() {
    return {
      importedYaml: null,
    }
  },
  methods: {
    parseYaml() {
      let rawYaml = this.$refs['yamlInput'].value;
      try {
        let parsedYaml =  jsyaml.load(rawYaml);
        store.commit('updateImportedYaml', parsedYaml);
      } catch (e) {
        let errorMessage;
        if ('reason' in e) {
          errorMessage = e.reason;
          errorMessage = errorMessage.charAt(0).toUpperCase() + errorMessage.slice(1) + '.';
          let alertWrapper = document.getElementById('import-alert');
          let alertContent = document.createElement('div');
          alertContent.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">${errorMessage}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
          alertWrapper.append(alertContent);
          store.commit('disableImportButton', false);
        }
      }
    },
  }
}
</script>

<style scoped>

</style>