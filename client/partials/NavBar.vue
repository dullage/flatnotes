<template>
  <nav class="flex justify-between">
    <Logo></Logo>
    <div>
      <Button label="Toggle Theme" @click="toggleTheme"></Button>
    </div>
  </nav>
</template>

<script setup>
import Button from "/components/Button.vue";
import Logo from "/components/Logo.vue";

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
}
</script>
