<template>
  <div class="container mx-auto flex h-screen flex-col px-2 py-4">
    <PrimeToast />
    <SearchModal ref="searchModal" />
    <NavBar
      v-if="showNavBar"
      ref="navBar"
      :hide-logo="!showNavBarLogo"
      @toggleSearchModal="toggleSearchModal"
    />
    <RouterView />
  </div>
</template>

<script setup>
import Mousetrap from "mousetrap";
import { useToast } from "primevue/usetoast";
import { computed, ref } from "vue";
import { RouterView, useRoute } from "vue-router";

import { getConfig, apiErrorHandler } from "./api.js";
import PrimeToast from "./components/PrimeToast.vue";
import { useGlobalStore } from "./globalStore.js";
import { loadTheme } from "./helpers.js";
import NavBar from "./partials/NavBar.vue";
import SearchModal from "./partials/SearchModal.vue";
import { loadStoredToken } from "./tokenStorage.js";

const globalStore = useGlobalStore();
const navBar = ref();
const route = useRoute();
const searchModal = ref();
const toast = useToast();

// '/' to search
Mousetrap.bind("/", () => {
  if (route.name !== "login") {
    toggleSearchModal();
    return false;
  }
});

getConfig()
  .then((data) => {
    globalStore.authType = data.authType;
  })
  .catch((error) => {
    apiErrorHandler(error, toast);
  });

loadStoredToken();

const showNavBar = computed(() => {
  return route.name !== "login";
});

const showNavBarLogo = computed(() => {
  return route.name !== "home";
});

function toggleSearchModal() {
  searchModal.value.toggle();
}

loadTheme();
</script>
