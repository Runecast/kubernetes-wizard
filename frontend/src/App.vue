<template>
  <div id="app">
    <AppHeader/>
    <div class="container-fluid">
      <div class="row m-2">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader";
import "/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"

export default {
  components: {AppHeader},
  created() {
    document.title = 'Runecast Kubernetes Wizard'
  },
}
</script>

<style>
@import './css/main.css?version=0.1';
@import './css/highlight.min.css?version=0.1';
@import './css/custom.css?version=0.1';
</style>
