<template>
  <div class="container mx-auto flex h-screen flex-col px-2 py-4">
    <PrimeToast />
    <NavBar v-if="showNavBar" :hide-logo="!showNavBarLogo" />
    <RouterView />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { RouterView, useRoute } from "vue-router";

import { getConfig } from "./api.js";
import { useGlobalStore } from "./globalStore.js";
import NavBar from "./partials/NavBar.vue";
import { loadStoredToken } from "./tokenStorage.js";
import PrimeToast from "./components/PrimeToast.vue";

const globalStore = useGlobalStore();
const route = useRoute();

getConfig()
  .then((data) => {
    globalStore.authType = data.authType;
  })
  .catch(function (error) {
    if (!error.handled) {
      // TODO: Trigger unknown error toast
      console.error(error);
    }
  });
loadStoredToken();

const showNavBar = computed(() => {
  return route.name !== "login";
});

const showNavBarLogo = computed(() => {
  return route.name !== "home";
});
</script>
