<template>
  <form class="flex w-full max-w-[500px]" v-on:submit.prevent="search">
    <input
      type="text"
      class="rounded rounded-r-none border border-theme-border bg-theme-background-elevated px-3 py-2 w-full focus:outline-none focus:ring-1"
      placeholder="Search"
    />
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

function search() {
  console.log("searching...");  // TODO: Implement search functionality
}
</script>
