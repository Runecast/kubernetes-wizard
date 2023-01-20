<template>
<code>
  {{ userInput }}
</code>
</template>

<script>
import store from "@/store";
import k8sVersions from "../../../config/k8s.json";

export default {
  name: "YamlWrapper",
  data() {
    return {
      versions: k8sVersions,
      userInput: store.state.userInput
    }
  },
}
</script>

<style scoped>

</style>