import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    k8sVersion: 'latest',
    jsonData: null,
    resource: null,
    excludedLists: ['common-definitions.quantity', 'map[string]Quantity'],
    userInput: {},
    importedYaml: null,
    parsedData: '',
    formUpdated: 0,
    importButtonDisabled: false,
    modification: {'reference': '', 'attribute': '', 'action': '', 'value': ''},
    parsedModifications: '',
    statusSectionIgnored: false,
  },
  getters: {
    displayVersion(state) {
      return state.k8sVersion.replace('-', '.')
    },
  },
  mutations: {
    changeVersion(state, version) {
      return state.k8sVersion = version
    },
    updateJsonData(state, data) {
      return state.jsonData = data
    },
    selectResource(state, resource) {
      return state.resource = resource
    },
    updateUserInput(state, userInput) {
      return state.userInput = userInput
    },
    updateParsedData(state, parsedData) {
      return state.parsedData = parsedData
    },
    updateImportedYaml(state, importedYaml) {
      return state.importedYaml = importedYaml
    },
    updateFormUpdated(state, formUpdated) {
      return state.formUpdated = formUpdated
    },
    disableImportButton(state, disabled) {
      return state.importButtonDisabled = disabled
    },
    updateModification(state, new_value) {
      return state.modification = new_value
    },
    updateParsedModifications(state, value) {
      state.parsedModifications = value
    },
    updateStatusSectionIgnored(state, value) {
      state.statusSectionIgnored = value
    }
  },
  actions: {
  },
  modules: {
  }
})
