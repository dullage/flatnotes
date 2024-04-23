<template>
  <div>
    <NavBar />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import NavBar from "/partials/NavBar.vue";
</script>
