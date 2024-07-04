<template>
  <button
    class="text-nowrap rounded px-2 py-1"
    :class="{
      'bg-theme-background text-theme-text-muted hover:bg-theme-background-elevated':
        style === 'subtle',
      'border bg-theme-background hover:bg-theme-background-elevated':
        style === 'cta',
      'border border-theme-danger text-theme-danger hover:bg-theme-danger/10':
        style === 'danger',
      'border border-theme-success text-theme-success hover:bg-theme-success/10':
        style === 'success',
    }"
  >
    <slot></slot>
    <IconLabel :iconPath="iconPath" :iconSize="iconSize" :label="label" />
  </button>
</template>

<script setup>
import IconLabel from "./IconLabel.vue";

defineProps({
  iconPath: String,
  iconSize: String,
  label: String,
  style: {
    type: String,
    default: "subtle",
    validator: (value) => {
      return ["subtle", "cta", "danger", "success"].includes(value);
    },
  },
});
</script>
