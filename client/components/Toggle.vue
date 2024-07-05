<template>
  <button
    class="flex cursor-pointer items-center text-nowrap rounded bg-theme-background px-2 py-1"
  >
    <span v-if="label" class="mr-2 text-theme-text-muted">{{ label }}</span>
    <SvgIcon
      type="mdi"
      :path="isOn ? mdiToggleSwitch : mdiToggleSwitchOff"
      :class="{ 'text-theme-brand': isOn, 'text-theme-text-very-muted': !isOn }"
      width="auto"
      height="1em"
      viewBox="2 7 20 10"
    ></SvgIcon>
  </button>
</template>

<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiToggleSwitch, mdiToggleSwitchOff } from "@mdi/js";

defineProps({
  label: String,
  isOn: Boolean,
});
</script>
