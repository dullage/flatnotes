<template>
  <input
    type="text"
    class="w-full rounded-md border border-theme-border px-3 py-2 focus:outline-none dark:bg-theme-background-elevated"
    v-model="model"
    ref="input"
  />
</template>

<script setup>
import { ref } from "vue";

const model = defineModel();
const input = ref();
</script>
