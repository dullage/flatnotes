<template>
  <button
    class="rounded px-2 py-1 text-theme-text-muted hover:bg-theme-background-tint hover:dark:bg-theme-background-elevated"
  >
    <IconLabel :iconPath="iconPath" :iconSize="iconSize" :label="label" />
  </button>
</template>

<script setup>
import IconLabel from "./IconLabel.vue";

defineProps({
  iconPath: String,
  iconSize: String,
  label: String,
});
</script>
