<template>
  <button
    class="hover:bg-theme-background-hover flex items-center rounded px-2 py-1 text-theme-text-muted"
  >
    <SvgIcon
      v-if="iconPath"
      type="mdi"
      :path="iconPath"
      size="1.25em"
      class="mr-1"
    ></SvgIcon>
    <span>{{ label }}</span>
  </button>
</template>

<script setup>
import SvgIcon from "@jamescoyle/vue-icon";

defineProps({
  iconPath: String,
  label: String,
});
</script>
