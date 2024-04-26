<template>
  <nav class="flex justify-between">
    <RouterLink to="/">
      <Logo :class="{ invisible: hideLogo }"></Logo>
    </RouterLink>
    <div class="flex">
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

const router = useRouter();

defineProps({
  hideLogo: Boolean,
});

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
}

function logOut() {
  router.push({ name: "login" });
  // TODO: Implement log out functionality
}
</script>
