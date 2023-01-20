<template>
<div id="result-wrapper">
  <div class="row">
    <h2 class="display-6 text-center">
      YAML Manifest <ActionButtons/>
    </h2>
    <ImportModal/>
  </div>
  <div id="import-alert"></div>
  <pre><code class="hljs" v-html="yamlUserInput"></code></pre>

</div>
</template>

<script>
import ActionButtons from "@/components/K8sWizard/ActionButtons";
import ImportModal from "@/components/K8sWizard/ImportModal";
import store from "@/store";
import jsyaml from "@/js-yaml.min"
import hljs from '@/highlight.min.js'

export default {
  name: "OutputWrapper",
  components: {ActionButtons, ImportModal},
  computed: {
    jsonUserInput() {
      return store.state.userInput
    },
    yamlUserInput() {
      let parsedData = this.parsedDataDisplay(this.jsonUserInput).trim();
      store.commit('updateParsedData', parsedData);
      return hljs.highlight(parsedData, {language: 'yaml'}).value;
    }
  },
  methods: {
    parsedDataDisplay(jsonUserInput) {
      let dumpedData = JSON.stringify(jsonUserInput, null, 4);
      if (dumpedData === '{}') {
        return ''
      } else {
        return jsyaml.dump(jsyaml.load(dumpedData, 'json'))
      }
    }
  }
}
</script>

<style scoped>
</style>