<template>
  <div>
    <h2 class="display-6 text-center">{{ resourceDisplay }}</h2>
    <form
      id="param-browser"
      class="m-3"
      @change="updateUserInput"
    >
      <DataObject
        :parameterData="parameterData"
        :is-list="false"
        :id-path="['param']"
        :select-one="null"
        ref="ref-param"
      />
    </form>
  </div>
</template>

<script>
import store from "@/store";
import DataObject from "@/components/K8sWizard/DataObject";

export default {
  name: "ParameterBrowser",
  components: {DataObject},
  data() {
    return {
      resource: null,
      previousMapKey: [],
    }
  },
  created() {
    let resource = store.state.resource;
    if (!resource) {  // Prevent browse to '/wizard' by hand
      this.$router.push({'path': '/'});
    }
    else {
      this.resource = resource;
    }
  },
  mounted() {
    this.updateUserInput();
  },
  computed: {
    resourceDisplay() {
      if (this.resource) {
        return this.resource.display
      }
      else return null
    },
    resourceKeySequence() {
      if (this.resource) {
        return [this.resource.section, this.resource.name, 'data_objects']
      }
      else return null
    },
    resourceData() {
      if (this.resource) {
        let data = store.state.jsonData
        this.resourceKeySequence.forEach(key => {
          data = data[key]
        })
        let keys = Object.keys(data);
        return {
          'keys': keys,
          'data': data
        }
      }
      else return null
    },
    parameterData() {
      if (this.resourceData) {
        let key = this.resourceData['keys'][0];
        let data = this.resourceData['data'];
        let dataMap = {}
        dataMap[key] = data[key]
        return data[key]
      }
      else return null
    },
    importedYaml() {
      return store.state.importedYaml;
    },
    formUpdated() {
      return store.state.importedYaml;
    },
  },
  watch: {
    importedYaml() {
      if (this.importedYaml !== '') {
        try {
           this.matchWithForm(this.importedYaml, this);
        } catch (e) {
          let errorMessage = JSON.stringify(e, null, 0)
          if (errorMessage === '{}') {
            errorMessage = `Some parameters were ignored.
            Please, verify that your YAML is correct, that you selected the proper resource and that you have set the correct version of Kubernetes.`
            let alertContent = document.createElement('div');
            alertContent.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">${errorMessage}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
            let alertWrapper = document.getElementById('import-alert');
            alertWrapper.append(alertContent);
            document.getElementById('import-button').disabled = false;
          }
        }
        if (store.state.statusSectionIgnored) {
          store.commit('updateStatusSectionIgnored', false);
          let warningMessage = `The "status" section has been ignored.`
          let alertContent = document.createElement('div');
          alertContent.innerHTML = `<div class="alert alert-warning alert-dismissible fade show" role="alert">${warningMessage}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
          let alertWrapper = document.getElementById('import-alert');
          alertWrapper.append(alertContent);
          document.getElementById('import-button').disabled = false;
        }
      }
      this.updateUserInput(true);
    },
  },
  methods: {
    Object_assign(target, ...sources) {
      sources.forEach(source => {
        Object.keys(source).forEach(key => {
          const s_val = source[key];
          const t_val = target[key];
          target[key] = t_val && s_val && typeof t_val === 'object' && typeof s_val === 'object'
                      ? this.Object_assign(t_val, s_val)
                      : s_val
        })
      })
      return target
    },
    isArrayOfNumbers(arr) {
      let isAllNumbers = false
      arr.forEach( (element) => {
        if (/^\d+$/.test(element)) {
          isAllNumbers = true
        }
      })
      return isAllNumbers

    },
    isArrayOfMapIndices(arr) {
      let isAllMapIndices = true
      arr.forEach( (element) => {
        if (!/^m\d+$/.test(element)) {
          isAllMapIndices = false
        }
      })
      return isAllMapIndices
    },
    convertToArraysOrMaps(obj) {
      /*
      The JSON obtained from the form doesn't have the same structure as the expected YAML:
       - lists are dictionaries with integers as keys
       - maps are dictionaries with integers preceded by the letter 'm' as keys
      This function recursively go through the Object containing the parsed data and finds such structure to replace them
      and returns an Object with the expected structure.
      */
      if (typeof obj === 'object' && obj !== null) {
        // Handle arrays
        let objectKeys = Object.keys(obj);
        let isAllNumbers = this.isArrayOfNumbers(objectKeys);
        let isAnyMapIndices = this.isArrayOfMapIndices(objectKeys);
        if (isAllNumbers) {
          obj = Object.values(obj)
          obj.forEach( (element, index) => {
            obj[index] = this.convertToArraysOrMaps(element)
          })
        }
        else if (isAnyMapIndices) {
          // Handle maps
          Object.keys(obj).forEach( (key) => {
            if (/m\d+/.test(key)) {
              let inMap = obj[key]
              let newKey = Object.keys(inMap)[0];
              obj[newKey] = this.convertToArraysOrMaps(inMap[newKey]);
              delete obj[key];
            }
          })
        }
        else {
          // Check next level of nesting
          Object.values(obj).forEach( (element, index) => {
            obj[objectKeys[index]] = this.convertToArraysOrMaps(element)
          })
        }
      }
      // Exit condition: not an object
      return obj
    },
    updateUserInput(disableImport) {
      if (disableImport) { store.commit('disableImportButton', true); }
      let userInput = {}
      let paramBrowser = document.getElementById('param-browser');
      for (let i=0; i<paramBrowser.length; i++ ) {
        let parameter = paramBrowser[i];
        if (parameter.id.startsWith('MAPKEY')) {
          if (parameter.value) {
            let oldId = paramBrowser[i+1].id;
            let newId = oldId.split('-');
            newId[newId.length-1] = parameter.value.replaceAll('-', 'H3767408609385598158');
            paramBrowser[i+1].id = newId.join('-');
          }
        }
        else if (parameter.id.startsWith('LISTMAPKEY-')){
          // Keys of map[string][]... objects are not registered but modify the index of the next inputs (values)
          if (parameter.value) {
            // Change ID of next fields
            let j = 1;
            while (paramBrowser[i+j].tagName === 'INPUT') {
              let oldId = paramBrowser[i+j].id;
              let splitNewId = oldId.split('-');
              splitNewId[splitNewId.length - 2] = parameter.value.replaceAll('-', 'H3767408609385598158');
              paramBrowser[i+j].id = splitNewId.join('-');
              j+=2
            }
          }
        }
        else if (parameter.id.startsWith('param-')) {
          if (parameter.value) {
            let pathList = parameter.id.split('-');
            pathList.shift();
            pathList.forEach( (key, index) => {
              pathList[index] = key.replaceAll('H3767408609385598158', '-')
            })

            let parameterValue;
            if (parameter.value === 'true' || parameter.value === 'false') {
              parameterValue = (parameter.value === 'true');
            } else if (!isNaN(parameter.value) && !isNaN(parseFloat(parameter.value))) {
              parameterValue = parseFloat(parameter.value);
            } else {
              parameterValue = parameter.value;
            }

            userInput = this.Object_assign({}, userInput, pathList.reduceRight(
                function (pastResult, currentKey) {
                  let obj = {};
                  obj[currentKey] = pastResult;
                  return obj;
                }, parameterValue)
            )
          }
        }
      }
      store.commit('updateUserInput', this.convertToArraysOrMaps(userInput));
    },
    sortMap(data) {
      return Object.keys(data).sort().reduce(
        (obj, key) => {
          obj[key] = data[key];
          return obj;
        }, {}
      );
    },
    sortArbitraryObject(data) {
      if (data instanceof Object && !(data instanceof Array)) {
        data = this.sortMap(data)
        Object.keys(data).forEach( key => {
          data[key] = this.sortArbitraryObject(data[key]);
        })
      }
      else if (data instanceof Object && data instanceof Array) {
        if (data.length && data[0] instanceof Object) {
          data = data.sort((a, b) => a < b ? -1 : 1);
          data.forEach( (element, index) => {
            data[index] = this.sortArbitraryObject(element)
          })
        }
        else {
          data = data.sort();
        }
      }
      return data
    },
    matchWithForm(data, component, previousKeys) {
      let input;
      if (previousKeys === undefined) {  // Initial call
        previousKeys = [];
      }
      if (data instanceof Object && !(data instanceof Array)) {
        Object.keys(data).forEach((key) => {
          if (key === 'status') {
            store.commit('updateStatusSectionIgnored', true);
          }
          else {
            let childRef = ['ref', 'param', ...previousKeys].join('-')
            let child = component.$refs[childRef]
            child = child instanceof Array ? child[0] : child
            if (child === undefined) {  // SelectOne
              let selected = previousKeys[previousKeys.length - 1]
              component.setSelectOne(selected);
              child = component.$refs[childRef]
              child = child instanceof Array ? child[0] : child
            }
            if (child.$options.name === 'AnyInput') {
              // SimpleMap or ListMap
              child = child.$refs[childRef];
            }

            this.matchWithForm(data[key], child, previousKeys.concat(key));
          }
        })
      }
      else if (data instanceof Object && data instanceof Array) {
        data.forEach( (value, index) => {
          let childRef = ['ref', 'param', ...previousKeys].join('-')
          let childListRef = ['ref', 'param', ...previousKeys, index].join('-')
          let child;
          if (Object.keys(component.$refs).includes(childRef)) {
            child = component.$refs[childRef];
          }
          else if (Object.keys(component.$refs).includes(childListRef)){
            child = component.$refs[childListRef];
          }
          else {
            component.incrementIndicesList(previousKeys[previousKeys.length-1])
            if (Object.keys(component.$refs).includes(childRef)) {
              child = component.$refs[childRef];
            }
            else if (Object.keys(component.$refs).includes(childListRef)) {
              child = component.$refs[childListRef];
            }
          }
          child = child instanceof Array? child[0]: child;
          if (child.$options.name === 'AnyInput') {  // if (Object.keys(child.$refs).includes(childRef)) {
            // Contains SimpleInputList
            child = child.$refs[childRef];
            this.matchWithForm(value, child, previousKeys.concat(index));
          }
          else {  // DataObject
            Object.keys(value).forEach( (key) => {
              this.matchWithForm(value[key], child, [...previousKeys, index, key]);
            })
          }
        })
      }
      else {  // Final value (not an Object or an Array)
        if (component.$options.name === 'DataObject' || component.$options.name === 'AnyInput') {
          let childRef = ['ref', 'param', ...previousKeys].join('-');
          if (Object.keys(component.$refs).includes(childRef)) {
            let child = component.$refs[childRef];
            child = child instanceof Array? child[0]: child;
            this.matchWithForm(data, child, previousKeys);
          }
        }
        else {
          if (component.$options.name === 'SimpleMap') {
            let index = component.$refs.key.length - 1;
            if (component.$refs.key[index] !== '') {
              component.incrementIndicesList();
              index ++;
            }
            component.setKey(previousKeys[previousKeys.length-1], index);
            component.setValue(data, index);
          }
          if (component.$options.name === 'ListMap') {
            let index = component.$refs.key.length - 1;
            if (component.$refs.key[index] !== '') {
              component.incrementIndicesList();
              index ++;
            }
            component.setKey(previousKeys[previousKeys.length-1], index);
            component.setValue(data, index);
          }
          else {
            let parameterId = 'param-' + previousKeys.join('-');
            input = document.getElementById(parameterId);
            if (!input && typeof previousKeys[previousKeys.length - 1] === 'number') {
              component.incrementIndicesList();
              component.setValueOfLastInput(data);
            } else if (input) {
              if (Object.keys(component.$refs).includes('input') && component.$refs['input'] instanceof Array) {
                component.setValueOfLastInput(data);
              } else if (Object.keys(component.$refs).includes('input') && !(component.$refs['input'] instanceof Array)) {
                component.setInputValue(data);
              }
            }
          }
        }
      }
    },
  },
}
</script>

<style scoped>

</style>