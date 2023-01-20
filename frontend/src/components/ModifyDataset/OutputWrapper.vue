<template>
<div>
  <div class="row">
    <h2 class="display-6 text-center">
      Generated modification <CopyButton/>
    </h2>
  </div>
  <pre><code class="hljs" v-html="yamlUserInput"></code></pre>
</div>
</template>

<script>

import store from "@/store";
import jsyaml from "@/js-yaml.min"
import hljs from '@/highlight.min.js'
import CopyButton from "@/components/ModifyDataset/CopyButton";

export default {
  name: "OutputWrapper",
  components: {CopyButton},
  computed: {
    userInput() {
      let values = {}
      Object.keys(store.state.modification).forEach( (key) => {
        let value = store.state.modification[key];
        if (value) {
          values[key] = value
        }
      })
      if (store.state.modification['value'] instanceof Array && !store.state.modification['value'].length) {
        delete values['value']
      }
      return values;
    },
    yamlUserInput() {
      let userInputAsArray = Object.keys(this.userInput).length? [this.userInput]: this.userInput;
      let dumpedData = JSON.stringify(userInputAsArray, null, 4);
      let parsedData = ''
      if (dumpedData !== '{}') {
        parsedData = jsyaml.dump(jsyaml.load(dumpedData, 'json')).trim();
      }
      store.commit('updateParsedModifications', parsedData)
      return hljs.highlight(parsedData, {language: 'yaml'}).value;
    }
  }
}
</script>

<style scoped>

</style>