<template>
  <form class="flex w-full max-w-[500px]" @submit.prevent="search">
    <TextInput placeholder="Search" class="rounded-r-none" />
    <ButtonComponent
      :iconPath="mdilMagnify"
      iconSize="1.75em"
      class="rounded-l-none border border-l-0 border-theme-border focus:outline-none focus:ring-1"
    />
  </form>
</template>

<script setup>
import { mdilMagnify } from "@mdi/light-js";

import ButtonComponent from "./ButtonComponent.vue";
import TextInput from "./TextInput.vue";

function search() {
  console.log("searching...");  // TODO: Implement search functionality
}
</script>
