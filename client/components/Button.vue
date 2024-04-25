<template>
  <button
    class="hover:bg-theme-background-hover flex items-center rounded px-2 py-1 text-theme-text-muted"
  >
    <SvgIcon
      v-if="iconPath"
      type="mdi"
      :path="iconPath"
      :size="iconSize"
      :class="{ 'mr-1': label }"
    ></SvgIcon>
    <span v-if-label>{{ label }}</span>
  </button>
</template>

<script setup>
import SvgIcon from "@jamescoyle/vue-icon";

defineProps({
  iconPath: String,
  iconSize: {
    type: String,
    default: "1.25em",
  },
  label: String,
});
</script>
