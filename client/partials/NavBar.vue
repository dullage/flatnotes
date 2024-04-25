<template>
  <nav class="flex justify-between">
    <Logo></Logo>
    <div>
      <Button
        :iconPath="mdilPlusCircle"
        label="New Note"
        @click="toggleTheme"
      ></Button>
    </div>
  </nav>
</template>

<script setup>
import { mdilPlusCircle } from "@mdi/light-js";

import Button from "/components/Button.vue";
import Logo from "/components/Logo.vue";

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
}
</script>
