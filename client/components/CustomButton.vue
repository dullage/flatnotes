<template>
  <button
    class="rounded px-2 py-1 hover:bg-theme-background-tint hover:dark:bg-theme-background-elevated"
    :class="{
      'text-theme-text-muted': !isCta,
      'border border-theme-border': isCta,
    }"
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
  isCta: Boolean,
});
</script>
