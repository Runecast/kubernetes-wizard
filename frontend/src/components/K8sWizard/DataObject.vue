<template>
<div>
  <div v-if="objectDescriptions" v-html="`${objectDescriptions}<hr>`">
  </div>
  <div
    class="mt-3 mb-3"
    v-for="(key, index) in subParameters"
    :key="key"
  >
    <!-- Composite Object -->
    <div
      v-if="subParameterDetails[key]['reference'] && subParameterDetails[key]['reference'] !== 'common-definitions.quantity'  && (!selectOne || !selectOne.includes(key))"
      :id="`accordion-${getDisplayIdFromPath(key)}`"
      class="accordion"
    >
      <div
        class="accordion-item"
        v-for="itemIndex in indices[key]"
        :key="itemIndex"
      >
        <!-- Accordion for list -->
        <div v-if="subParameterDetails[key]['isList']">
          <h2 class="accordion-header" :id="`heading-${getDisplayListIdFromPath(key, itemIndex)}`">
            <div
                class="btn-group w-100"
                role="group"
                aria-label="Header button group"
            >
              <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                aria-expanded="false"
                :data-bs-target="`#collapse-${getDisplayListIdFromPath(key, itemIndex)}`"
                :aria-controls="`collapse-${getDisplayListIdFromPath(key, itemIndex)}`"
              >
                <span class="text-primary">{{ key }}</span>&nbsp;<span v-if="subParameterDetails[key]['required']" class="text-secondary">(required)</span>
              </button>
              <a
                v-if="indices[key].length > 1"
                @click="removeAccordionItem(key, itemIndex)"
                type="button"
                class="close text-muted btn-light-grey button-close disabled"
                aria-label="Close"
              >
                <span class="p-3 button-close-icon">&times;</span>
              </a>
            </div>
          </h2>

          <div
            class="accordion-collapse collapse"
            :id="`collapse-${getDisplayListIdFromPath(key, itemIndex)}`"
            :aria-labelledby="`heading-${getDisplayListIdFromPath(key, itemIndex)}`"
            :data-bs-parent="`#accordion-${getDisplayIdFromPath(key)}`"
          >
            <div class="accordion-body">
              <div v-if="parameterDescriptions[key]" v-html="parameterDescriptions[key]"></div>
              <DataObject
                v-if="subParameterDetails[key]['reference'] && (!subParameterDetails[key]['select_one']  || !subParameterDetails[key]['select_one'].includes(key))"
                :parameter-data="subParameterData(subParameterDetails[key]['reference'])"
                :id-path="getListIdFromPath(key, itemIndex)"
                :select-one="subParameterDetails[key]['select_one']"
                :ref="'ref-' + getDisplayListIdFromPath(key, itemIndex)"
              />
            </div>
          </div>
        </div>
        <!-- Accordion with unique item -->

        <div v-else-if="!subParameterDetails[key]['isList']">
          <h2 class="accordion-header" :id="`heading-${getDisplayIdFromPath(key)}`">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="`#collapse-${getDisplayIdFromPath(key)}`"
              aria-expanded="false"
              :aria-controls="`collapse-${getDisplayIdFromPath(key)}`"
            >
              <span class="text-primary">{{ key }}</span>&nbsp;<span v-if="subParameterDetails[key]['required']" class="text-secondary">(required)</span>
            </button>
          </h2>
          <div
            class="accordion-collapse collapse"
            :id="`collapse-${getDisplayIdFromPath(key)}`"
            :aria-labelledby="`heading-${getDisplayIdFromPath(key)}`"
            :data-bs-parent="`#accordion-${getDisplayIdFromPath(key)}`"
          >
            <div class="accordion-body">
              <div v-if="parameterDescriptions[key]" v-html="`${parameterDescriptions[key]}<hr>`"></div>
              <DataObject
                v-if="subParameterDetails[key]['reference'] && (!subParameterDetails[key]['select_one'])"
                :parameter-data="subParameterData(subParameterDetails[key]['reference'])"
                :id-path="getIdFromPath(key)"
                :select-one="subParameterDetails[key]['select_one']"
                :ref="'ref-' + getDisplayIdFromPath(key)"
            />
            </div>
          </div>
        </div>
      </div>
      <div
          v-if="subParameterDetails[key]['isList']"
          class="text-center mt-1"
      >
        <button
            class="btn btn-outline-primary"
            type="button"
            :id="`add-button-${getDisplayIdFromPath(key)}`"
            @click="incrementIndicesList(key)"
        >
          Add
        </button>
      </div>
    </div>

    <!-- Input -->
    <AnyInput
      v-if="(!subParameterDetails[key]['reference'] || subParameterDetails[key]['reference'] === 'common-definitions.quantity') && (!selectOne || !selectOne.includes(key))"
      :parameter-name="key"
      :parameterData="parameterData['parameters'][key]"
      :id-path="getIdFromPath(key)"
      :add-button-index="index"
      :type="subParameterDetails[key]['type']"
      :ref="`ref-${getDisplayIdFromPath(key)}`"
    />
  </div>

  <div v-if="selectOne">
    <select
      :id="getSelectOneIdFromPath()"
      :ref="getSelectOneIdFromPath()"
      v-model="selected"
      class="form-select"
    >
      <option selected :value="undefined">Select one</option>
      <option
        v-for="option in selectOne"
        :key="option"
        :value="option"
      >
        {{ option }}
      </option>
    </select>

    <div
      v-if="selected"
      :id="`accordion-${getDisplayIdFromPath(selected)}`"
      class="accordion pt-3"
    >
      <div
        class="accordion-item"
      >
        <h2 class="accordion-header" :id="`heading-${getDisplayIdFromPath(selected)}`">
          <div
              class="btn-group w-100"
              role="group"
              aria-label="Header button group"
          >
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              aria-expanded="false"
              :data-bs-target="`#collapse-${getDisplayIdFromPath(selected)}`"
              :aria-controls="`collapse-${getDisplayIdFromPath(selected)}`"
            >
              <span class="text-primary">{{ selected }}</span>&nbsp;<span v-if="subParameterDetails[selected]['required']" class="text-secondary">(required)</span>
            </button>
          </div>
        </h2>
        <div
          class="accordion-collapse collapse"
          :id="`collapse-${getDisplayIdFromPath(selected)}`"
          :aria-labelledby="`heading-${getDisplayIdFromPath(selected)}`"
          :data-bs-parent="`#accordion-${getDisplayIdFromPath(selected)}`"
        >
          <div class="accordion-body">
            <DataObject
              :parameter-data="subParameterData(subParameterDetails[selected]['reference'])"
              :id-path="[...idPath, selected]"
              :select-one="subParameterDetails[selected]['select_one']"
              :ref="['ref', ...idPath, selected].join('-')"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

</div>
</template>

<script>
import store from "@/store";
import AnyInput from "@/components/K8sWizard/AnyInput";

export default {
  name: "DataObject",
  components: {AnyInput},
  props: ['parameterData', 'idPath', 'selectOne'],
  data() {
    return {
      indices: {},
      objectDescriptions: {},
      parameterDescriptions: {},
      selected: undefined,
    }
  },
  created() {
    this.subParameters.forEach( key => { this.indices[key] = [0] })
    if (this.parameterData) {
      if (Object.keys(this.parameterData).includes('description')) {
        this.objectDescriptions = this.parameterData['description'] ? this.parameterData['description'].replaceAll(/(https?:\/\/[\w\-_./#?]+)/g, '<a href="$1" target="_blank">$1</a>') : null;
      }
      this.subParameters.forEach(key => {
        if (Object.keys(this.parameterData['parameters']).includes(key)) {
          this.parameterDescriptions[key] = this.parameterData['parameters'][key]['description'] ? this.parameterData['parameters'][key]['description'].replaceAll(/(https?:\/\/[\w\-_./#?]+)/g, '<a href="$1" target="_blank">$1</a>') : null;
        }
      })
    }
  },
  computed: {
    subParameters() {
      let parameterKeys = this.parameterData? Object.keys(this.parameterData): null;
      if (parameterKeys && parameterKeys.includes('parameters')) {
        return Object.keys(this.parameterData['parameters']).filter(parameterName => parameterName !== 'status')
      }
      else return []
    },
    subParameterDetails() {
      let details = {};
      this.subParameters.forEach( key => {
        let type = this.parameterData['parameters'][key]['type'] ? this.parameterData['parameters'][key]['type'] : '';
        details[key] = {
          'reference': Object.keys(this.parameterData['parameters'][key]).includes('reference') ? this.parameterData['parameters'][key]['reference'] : null,
          'type': type,
          'isList': type.startsWith('[]'),
          'required': Object.keys(this.parameterData['parameters'][key]).includes('required') ? this.parameterData['parameters'][key]['required']: false,
          'select_one': Object.keys(this.parameterData['parameters'][key]).includes('select_one') ? this.parameterData['parameters'][key]['select_one']: null,
        }
      })
      return details
    },
  },
  methods: {
    setSelectOne(selected) {
      this.selected = selected;
      this.$mount()
    },
    subParameterData(reference) {
      let data = store.state.jsonData;
      let keys = reference.split('.');
      keys.forEach( key => {
        data = data[key]
      })
      return data
    },
    removeAccordionItem(key, itemIndex) {
      this.indices[key].splice(this.indices[key].indexOf(itemIndex), 1);
      this.$mount();
      this.$root.$children[0].$children[1].$refs['parameter-browser'].updateUserInput();
    },
    incrementIndicesList(key) {
      let max = Math.max(...this.indices[key]);
      this.indices[key].push(max+1);
      // this.$forceUpdate();
      this.$mount();
    },
    getIdFromPath(key) {
      return this.idPath.concat(key)
    },
    getSelectOneIdFromPath() {
      return ['select-one', ...this.idPath.slice(1)].join('-')
    },

    getListIdFromPath(key, index) {
      return this.idPath.concat(key).concat(index)
    },
    getDisplayIdFromPath(key) {
      return this.getIdFromPath(key).join('-');
    },
    getDisplayListIdFromPath(key, index) {
      return this.getListIdFromPath(key, index).join('-');
    },
  }
}
</script>

<style scoped>

</style>