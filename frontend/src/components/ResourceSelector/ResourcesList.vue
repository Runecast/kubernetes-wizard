<template>
  <div id="resource-list">
    <h2 class="m-3 display-6 text-center">Resources ({{ displayK8sVersion }})</h2>
    <div class="m-2">
      <input type="text" class="control-form" placeholder="Filter" @keyup="updateFilter">
    </div>

    <div class="accordion accordion-flush" id="accordion">
      <ResourceButtons
        v-for="(section, index) in sections"
        :key="section + '-' + k8sVersion"
        :section="section"
        :index="index"
        :filter="filter"
        >
        {{ section }}
      </ResourceButtons>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ResourceButtons from "@/components/ResourceSelector/ResourceButtons";
import store from "@/store";

export default {
  name: "ResourcesList",
  components: {ResourceButtons},
  data () {
    return {
      sections: [],
      filter: '',
    }
  },
  computed: {
    k8sVersion() {
      return store.state.k8sVersion
    },
    jsonData() {
      return store.state.jsonData
    },
    displayK8sVersion() {
      return store.getters.displayVersion
    }
  },
  mounted() {
    this.fetchData()
  },
  watch: {
    k8sVersion() {
      this.fetchData();
    }
  },
  methods: {
    fetchData() {
      let protocol = location.protocol;
      let hostName = location.hostname;
      let port = location.port !== '8080'? (location.port? ':': '')+location.port: ':5000'  // Set port 5000 in dev mode
      let apiEndpoint = `${protocol}//${hostName}${port}/api_reference/${store.state.k8sVersion}`;
      axios
      .get(apiEndpoint)
      .then(response => (
          this.getJsonContent(response.data)
      ))
    },
    getJsonContent(jsonData) {
      store.commit('updateJsonData', jsonData);
      let sections = []
      if (jsonData) {
        Object.keys(jsonData).slice(0, -1).forEach((section) => {
          sections.push(section)
        })
      }
      this.sections = sections;
    },
    updateFilter(event) {
      this.filter = event.target.value.toLowerCase();
    },
  }
}
</script>

<style scoped>

</style>