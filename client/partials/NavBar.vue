<template>
  <nav class="flex justify-between">
    <RouterLink to="/">
      <Logo :class="{ invisible: hideLogo }"></Logo>
    </RouterLink>
    <div>
      <CustomButton
        :iconPath="mdilPlusCircle"
        label="New Note"
        @click="toggleTheme"
      />
    </div>
  </nav>
</template>

<script setup>
import { mdilPlusCircle } from "@mdi/light-js";
import { RouterLink } from "vue-router";

import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";

defineProps({
  hideLogo: Boolean,
});

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
}
</script>
