<template>
  <div id="header" class="nav-color d-sm-flex align-items-sm-center justify-content-sm-between px-4 sticky-top">
    <a href="javascript:void(0)" @click="goBackToResourceSelector">
      <h1 class="text-white d-sm-flex align-items-sm-end">
        <main-logo class="me-4" />
        <span class="small text-light-grey">Kubernetes Wizard</span>
      </h1>
    </a>
    <div class="text-light-grey">
      Made by
      <a
          href="https://www.runecast.com/"
          target="_blank"
          class="text-white text-decoration-underline"
      >
        runecast.com
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import MainLogo from '@/assets/MainLogo.vue';

export default Vue.extend({
  name: 'AppHeader',
  components: {
    MainLogo,
  },
  props: {
    msg: String,
  },
  methods: {
    goBackToResourceSelector() {
      if (this.$router.currentRoute.path !== '/') {
        this.$router.push({path: `/`});
      }
    }
  }
});
</script>

<style scoped lang="scss">
.nav-color {
  background: linear-gradient(90.14deg,#000b11 3.18%,#082c5e 50.12%);
}
</style>
