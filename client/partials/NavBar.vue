<template>
  <nav class="mb-12 flex justify-between align-top">
    <SearchModal ref="searchModal" />
    <RouterLink :to="{ name: 'home' }" v-if="!hideLogo">
      <Logo responsive></Logo>
    </RouterLink>
    <div class="flex grow items-start justify-end">
      <!-- New Note -->
      <RouterLink :to="{ name: 'note' }">
        <CustomButton :iconPath="mdilPlusCircle" label="New Note" />
      </RouterLink>
      <!-- Menu -->
      <CustomButton :iconPath="mdilMenu" label="Menu" @click="toggleMenu" />
      <PrimeMenu ref="menu" :model="menuItems" :popup="true" />
    </div>
  </nav>
</template>

<script setup>
import {
  mdilLogout,
  mdilPlusCircle,
  mdilMenu,
  mdilMagnify,
  mdilNoteMultiple,
  mdilMonitor,
} from "@mdi/light-js";
import { RouterLink, useRouter } from "vue-router";
import { ref } from "vue";

import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import { clearStoredToken } from "../tokenStorage.js";
import PrimeMenu from "../components/PrimeMenu.vue";
import SearchModal from "./SearchModal.vue";

const menu = ref();
const router = useRouter();
const searchModal = ref();

defineProps({
  hideLogo: Boolean,
});

const menuItems = [
  {
    label: "Search",
    icon: mdilMagnify,
    command: () => searchModal.value.toggle(),
  },
  {
    label: "All Notes",
    icon: mdilNoteMultiple,
    command: () => router.push({ name: "search", query: { term: "*" } }),
  },
  {
    label: "Toggle Theme",
    icon: mdilMonitor,
    command: toggleTheme,
  },
  {
    separator: true,
  },
  {
    label: "Log Out",
    icon: mdilLogout,
    command: logOut,
  },
];

function toggleTheme() {
  document.body.classList.toggle("dark");
}

function logOut() {
  clearStoredToken();
  router.push({ name: "login" });
}

function toggleMenu(event) {
  menu.value.toggle(event);
}
</script>
