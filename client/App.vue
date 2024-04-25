<template>
  <div class="container mx-auto flex h-screen flex-col px-2 py-4">
    <NavBar />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import NavBar from "/partials/NavBar.vue";
</script>
