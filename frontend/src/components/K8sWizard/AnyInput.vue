<template>
  <IntegerInput
    v-if="isInteger"
    :parameter-name="parameterName"
    :parameter-data="parameterData"
    :id-path="idPath"
    :ref="['ref', ...idPath].join('-')"
  />
  <BooleanInput
    v-else-if="isBoolean"
    :parameter-name="parameterName"
    :parameter-data="parameterData"
    :id-path="idPath"
    :ref="['ref', ...idPath].join('-')"
  />
  <SimpleInputList
    v-else-if="isList"
    :parameter-name="parameterName"
    :add-button-index="addButtonIndex"
    :parameter-data="parameterData"
    :id-path="idPath"
    :ref="['ref', ...idPath].join('-')"
  />
  <ListMap
      v-else-if="isListMap"
      :parameter-name="parameterName"
      :id-path="idPath"
      :parameter-data="parameterData"
  />
  <SimpleMap
      v-else-if="isMap"
      :parameter-name="parameterName"
      :parameter-data="parameterData"
      :id-path="idPath"
      :ref="['ref', ...idPath].join('-')"
  />
  <OptionsInput
    v-else-if="optionsList"
    :parameter-name="parameterName"
    :parameter-data="parameterData"
    :options="optionsList"
    :id-path="idPath"
    :ref="['ref', ...idPath].join('-')"
  />
  <SimpleInput
    v-else
    :parameter-name="parameterName"
    :parameter-data="parameterData"
    :id-path="idPath"
    :ref="['ref', ...idPath].join('-')"
  />
</template>

<script>
import IntegerInput from "@/components/K8sWizard/InputTypes/IntegerInput";
import BooleanInput from "@/components/K8sWizard/InputTypes/BooleanInput";
import SimpleInput from "@/components/K8sWizard/InputTypes/SimpleInput";
import SimpleInputList from "@/components/K8sWizard/InputTypes/SimpleInputList";
import OptionsInput from "@/components/K8sWizard/InputTypes/OptionsInput";
import SimpleMap from "@/components/K8sWizard/InputTypes/SimpleMap";
import ListMap from "@/components/K8sWizard/InputTypes/ListMap";

export default {
  name: "AnyInput",
  components: {IntegerInput, BooleanInput, SimpleInput, SimpleInputList, OptionsInput, SimpleMap, ListMap},
  props: ['parameterName', 'idPath', 'addButtonIndex', 'parameterData', 'type'],
  data() {
    return {
      isInteger: this.type.startsWith('int'),
      isBoolean: this.type.startsWith('boolean') && this.parameterName !== 'quantity',
      isList: this.type.startsWith('[]'),
      isMap: this.type.startsWith('map[string]'),
      isListMap: this.type.startsWith('map[string][]'),
      optionsList: this.parameterData['options'],
    }
  },
}
</script>

<style scoped>

</style>