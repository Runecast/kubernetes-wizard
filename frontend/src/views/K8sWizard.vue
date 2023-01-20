<template>
  <div id="wizard" class="row">
    <div id="left-panel" class="col-md-6 overflow-auto">
      <ParameterBrowser ref="parameter-browser"/>
    </div>
    <hr class="d-md-none my-2">
    <div id="result-wrapper" class="col-md-6 overflow-auto">
      <OutputWrapper/>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import store from "@/store";
import OutputWrapper from "@/components/K8sWizard/OutputWrapper";
import ParameterBrowser from "@/components/K8sWizard/ParameterBrowser";

export default Vue.extend({
  name: 'ResourceSelector',
  components: {
    ParameterBrowser,
    OutputWrapper
  },
  data() {
    return {
      k8sVersion: store.state.k8sVersion,
      resource: null
    }
  },
  mounted() {
    function setHeight(path) {
      if (path === '/wizard') {
        let header = document.getElementById('header');
        let newHeight = window.innerHeight - header.offsetHeight - 25;
        document.getElementById('left-panel').style.height = newHeight + 'px';
        document.getElementById('result-wrapper').style.height = newHeight + 'px';
      }
    }
    setHeight(this.$router.currentRoute.path);
    window.addEventListener('resize', () => {
      setHeight(this.$router.currentRoute.path);
    })
  },
});
</script>
