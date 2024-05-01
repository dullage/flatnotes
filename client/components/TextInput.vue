<template>
  <input
    type="text"
    class="w-full rounded border border-theme-border bg-theme-background-elevated px-3 py-2 focus:outline-none focus:ring-1"
    placeholder="Search"
    v-model="model"
  />
</template>

<script setup>
const model = defineModel()
</script>
