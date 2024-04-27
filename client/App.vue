<template>
  <div class="container mx-auto flex h-screen flex-col px-2 py-4">
    <Toast class="ml-[20px]" :pt="toastStyle" position="bottom-right" />
    <NavBar v-if="showNavBar" :hide-logo="!showNavBarLogo" />
    <RouterView />
  </div>
</template>

<script setup>
import Toast from "primevue/toast";
import { computed, onBeforeMount } from "vue";
import { RouterView, useRoute } from "vue-router";

import { getConfig } from "./api.js";
import { useGlobalStore } from "./globalStore.js";
import NavBar from "./partials/NavBar.vue";
import { loadStoredToken } from "./tokenStorage.js";

const globalStore = useGlobalStore();
const route = useRoute();

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
  loadStoredToken();
});

const showNavBar = computed(() => {
  return route.name !== "login";
});

const showNavBarLogo = computed(() => {
  return route.name !== "home";
});

const toastStyle = {
  message: "flex flex-col items-end",
  container:
  "bg-theme-background-elevated border border-theme-border mb-2 px-3 py-2 rounded-lg max-w-96",
  icon: "invisible h-0 w-0",
  summary: "font-bold",
};
</script>
