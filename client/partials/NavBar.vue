<template>
  <nav class="mb-4 flex justify-between align-top">
    <RouterLink to="/" v-if="!hideLogo">
      <Logo></Logo>
    </RouterLink>
    <div class="flex grow items-start justify-end">
      <CustomButton
        :iconPath="mdilPlusCircle"
        label="New Note"
        @click="toggleTheme"
      />
      <CustomButton :iconPath="mdilLogout" label="Log Out" @click="logOut" />
    </div>
  </nav>
</template>

<script setup>
import { mdilLogout, mdilPlusCircle } from "@mdi/light-js";
import { RouterLink, useRouter } from "vue-router";

import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import { clearStoredToken } from "../tokenStorage.js";

const router = useRouter();

defineProps({
  hideLogo: Boolean,
});

function toggleTheme() {
  document.body.classList.toggle("dark");
}

function logOut() {
  clearStoredToken();
  router.push({ name: "login" });
}
</script>
