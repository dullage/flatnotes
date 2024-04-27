<template>
  <div class="container mx-auto flex h-screen flex-col px-2 py-4">
    <RouterView />
  </div>
</template>

<script setup>
import { onBeforeMount } from "vue";
import { RouterView } from "vue-router";

import { getConfig } from "./api.js";
import { useGlobalStore } from "./globalStore.js";

const globalStore = useGlobalStore();

onBeforeMount(() => {
  getConfig()
    .then((response) => {
      globalStore.authType = response.data.authType;
    })
    .catch(function (error) {
      if (!error.handled) {
        // TODO: Trigger unknown error toast
        console.error(error);
      }
    });
});
</script>
