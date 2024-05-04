<template>
  <!-- Mask -->
  <div
    class="fixed left-0 top-0 z-50 flex h-dvh w-dvw items-center justify-center bg-theme-background-tint/40 backdrop-blur-sm"
    :class="{ hidden: !isVisible }"
  >
    <!-- Modal -->
    <div
      class="max-w-96 grow rounded-lg border border-theme-border bg-theme-background px-6 py-4 shadow-lg"
      :class="$attrs.class"
    >
      <!-- Title -->
      <div class="mb-6 flex justify-between">
        <div class="text-xl">{{ title }}</div>
        <CustomButton :iconPath="mdiWindowClose" @click="close" />
      </div>
      <!-- Slot -->
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { mdiWindowClose } from "@mdi/js";

defineOptions({
  inheritAttrs: false,
});

const props = defineProps({
  closeHandler: Function,
  modalClasses: String,
  title: String,
});

import CustomButton from "./CustomButton.vue";

const isVisible = ref(false);

function toggle() {
  isVisible.value = !isVisible.value;
}

function setVisibility(value) {
  isVisible.value = value;
}

function close() {
  if (props.closeHandler) {
    props.closeHandler();
  } else {
    setVisibility(false);
  }
}

defineExpose({ toggle, setVisibility });
</script>
