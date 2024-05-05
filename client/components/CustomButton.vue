<template>
  <button
    class="rounded px-2 py-1"
    :class="{
      'bg-theme-background text-theme-text-muted hover:bg-theme-background-elevated':
        !danger,
      'bg-theme-danger hover:bg-theme-danger/80 text-slate-50': danger,
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
  danger: Boolean,
});
</script>
