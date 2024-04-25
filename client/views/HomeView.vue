<template>
  <div class="h-full">
    <NavBar hide-logo />
    <div class="flex h-full flex-col items-center justify-center">
      <Logo class="mb-5" />
      <SearchInput class="shadow-[0_0_20px] shadow-theme-shadow" />
    </div>
  </div>
</template>

<script setup>
import Logo from "../components/Logo.vue";
import SearchInput from "../components/SearchInput.vue";
import NavBar from "../partials/NavBar.vue";
</script>
