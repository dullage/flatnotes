<template>
  <form class="flex" v-on:submit.prevent="search">
    <input
      type="text"
      class="rounded rounded-r-none border border-theme-border bg-theme-background-elevated px-3 py-2"
      placeholder="Search"
    />
    <Button
      :iconPath="mdilMagnify"
      iconSize="1.75em"
      class="rounded-l-none border border-l-0 border-theme-border"
    />
  </form>
</template>

<script setup>
import Button from "./Button.vue";
import { mdilMagnify } from "@mdi/light-js";

function search() {
  console.log("searching...");
}
</script>
