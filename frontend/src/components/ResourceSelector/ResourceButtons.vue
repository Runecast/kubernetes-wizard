<template>
  <div class="accordion-item" v-if="isNotEmpty">
    <h2 class="accordion-header" :id="headingId">
      <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          aria-expanded="false"
          :data-bs-target="'#'+collapseId"
          :aria-controls="collapseId"
      >
        {{ sectionNameDisplay }} ({{ resourceCount }})
      </button>
    </h2>
    <div
        class="accordion-collapse collapse"
        data-bs-parent="#accordion"
        :id="collapseId"
        :aria-labelledby="headingId"
    >
      <div class="accordion-body">
        <ul class="list-group">
          <li
              class="btn btn-secondary list-group-item"
              v-for="resource in filteredResources"
              :key="resource.raw"
              :resource="resource.raw"
              :id="'resource-button-'+resource.raw"
              @click="loadWizard"
          >
            {{ resource.display }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import store from "@/store";
import Vue from "vue";

export default Vue.extend({
  name: "ResourceButtons",
  props: {
    'section': String,
    'index': Number,
    'filter': String,
},
  computed: {
    jsonData() {
      return store.state.jsonData
    },
    headingId() {
      return `heading-${this.index}`
    },
    collapseId() {
      return `collapse-${this.index}`
    },
    resources() {
      let resourceList = [];
      let sectionContent = this.jsonData[this.section];
      Object.keys(sectionContent).forEach( resource => {
        resourceList.push(resource)
      })
      return resourceList
    },
    displayResource() {
      let displayResources = []
      this.resources.forEach( (resource) => {
        let display = resource.split('-')
        display.forEach((resource, index) => {
          if (index === display.length - 1) {
            display[index] = ' (' + resource + ')'
          } else {
            display[index] = resource.charAt(0).toUpperCase() + resource.slice(1);
          }
        })
        display = display.join('')
        displayResources.push(display)
      })
        return displayResources
    },
    filteredResources() {
      let filtered = []
      this.displayResource.forEach( (resource, index) => {
        if (
            resource.toLowerCase().includes(this.filter) &&
            /\(v\d(beta\d)?\)$/.test(resource)
        ) {
          filtered.push({'display': resource, 'raw': this.resources[index]})
        }
      })
        return filtered
    },
    resourceCount() {
      return this.filteredResources.length;
    },
    isNotEmpty() {
      return this.resourceCount > 0
    },
    sectionNameDisplay() {
      let section = this.section.replaceAll('-', ' ');
      return section.charAt(0).toUpperCase() + section.slice(1);
    }
  },
  methods: {
    loadWizard(event) {
      store.commit('selectResource', {
        'section': this.section,
        'name': event.target.attributes.resource.nodeValue,
        'display': event.target.innerText,
      })
      this.$router.push({'path': '/wizard'})
    }
  }
})
</script>

<style scoped>

</style>