<template>
<div>
  <h2 class="display-6 text-center">Modification form</h2>
  <form
    id="modification-form"
    class="m-3"
    @change="updateValues()"
    @submit.prevent
  >
    <ReferenceSelector
      :list="jsonData['references']"
      name="reference"
    />
    <SelectField
      :values="jsonData['attributes']"
      name="attribute"
    />
    <SelectField
      :values="jsonData['actions']"
      name="action"
    />
    <ScalarInput
      v-if="isScalar"
    />
    <ListInput
      v-if="isList"
    />
  </form>
</div>
</template>

<script>
import ReferenceSelector from "@/components/ModifyDataset/ReferenceSelector";
import axios from "axios";
import SelectField from "@/components/ModifyDataset/SelectField";
import ScalarInput from "@/components/ModifyDataset/ScalarInput";
import ListInput from "@/components/ModifyDataset/ListInput";
import store from "@/store";

export default {
  name: "ModificationForm",
  components: {ListInput, ScalarInput, SelectField, ReferenceSelector},
  mounted() {
    this.fetchData()
    // store.commit('updateModification', {})
  },
  data() {
    return {
      jsonData: {}
    }
  },
  computed: {
    isScalar() {
      return ['set scalar', 'append scalar'].includes(store.state.modification['action'])
    },
    isList() {
      return ['set list', 'concatenate list', 'remove items'].includes(store.state.modification['action'])
    }
  },
  methods: {
    fetchData() {
      let protocol = location.protocol;
      let hostName = location.hostname;
      let apiEndpoint = `${protocol}//${hostName}:5000/modifications`;
      axios
      .get(apiEndpoint)
      .then(response => (
          this.jsonData = response.data
      ))
    },
    updateValues() {
      let modificationForm = document.getElementById('modification-form');
      let newStoreValue = store.state.modification;
      let isList = ['set list', 'concatenate list', 'remove items'].includes(modificationForm[2].value)
      console.log('isList', isList)
      if (isList) {
        newStoreValue['value'] = []
      }
      else {
        newStoreValue['value'] = ''
      }
      for (let i=0; i< modificationForm.length; i++) {
        let field = modificationForm[i];
        if (field.id.startsWith('value') && isList) {
          newStoreValue['value'].push(field.value);
        }
        else if (!field.id.startsWith('value-')) {
          newStoreValue[field.id] = field.value;
        }
      }
      store.commit('updateModification', newStoreValue);
    },
  }
}
</script>

<style scoped>

</style>