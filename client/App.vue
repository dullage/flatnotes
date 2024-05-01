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
import { useToast } from "primevue/usetoast";

import { getConfig } from "./api.js";
import { useGlobalStore } from "./globalStore.js";
import NavBar from "./partials/NavBar.vue";
import { loadStoredToken } from "./tokenStorage.js";
import PrimeToast from "./components/PrimeToast.vue";
import { getUnknownServerErrorToastOptions } from "./helpers.js";

const globalStore = useGlobalStore();
const route = useRoute();
const toast = useToast();

getConfig()
  .then((data) => {
    globalStore.authType = data.authType;
  })
  .catch(() => {
    toast.add(getUnknownServerErrorToastOptions());
  });
loadStoredToken();

const showNavBar = computed(() => {
  return route.name !== "login";
});

const showNavBarLogo = computed(() => {
  return route.name !== "home";
});
</script>
