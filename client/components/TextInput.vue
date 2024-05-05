<template>
  <input
    type="text"
    class="w-full rounded border border-theme-border px-3 py-2 focus:outline-none focus:ring-1 dark:bg-theme-background-elevated"
    placeholder="Search"
    v-model="model"
    ref="input"
  />
</template>

<script setup>
import { ref } from "vue";

const model = defineModel();
const input = ref();

function focus() {
  input.value.focus();
}

defineExpose({ focus });
</script>
