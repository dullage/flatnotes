<template>
  <!-- Mask -->
  <div
    v-if="isVisible"
    class="fixed left-0 top-0 z-50 flex h-dvh w-dvw items-center justify-center bg-theme-background-tint/40 backdrop-blur-sm"
  >
    <!-- Modal -->
    <div
      class="relative max-w-[500px] grow rounded-lg border border-theme-border bg-theme-background px-6 py-4 shadow-lg"
      :class="$attrs.class"
    >
      <CustomButton
        :iconPath="mdiWindowClose"
        @click="close"
        class="absolute right-1 top-1"
      />
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
