<template>
  <!-- Mask -->
  <div
    v-if="isVisible"
    class="fixed left-0 top-0 z-50 flex h-dvh w-dvw items-center justify-center bg-slate-950/40 backdrop-blur-sm"
  >
    <!-- Modal -->
    <div
      class="relative max-w-[500px] grow rounded-lg border border-theme-border bg-theme-background px-6 py-4 shadow-lg"
      :class="$attrs.class"
    >
      <CustomButton
        v-if="props.showClose"
        :iconPath="mdiWindowClose"
        @click="close"
        class="absolute right-1 top-1"
      />
      <!-- Title -->
      <div class="mb-6 text-xl">{{ title }}</div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { mdiWindowClose } from "@mdi/js";
import { ref } from "vue";

import CustomButton from "./CustomButton.vue";

defineOptions({
  inheritAttrs: false,
});

const props = defineProps({
  title: { type: String, default: "Confirm" },
  showClose: { type: Boolean },
  closeHandler: Function,
  modalClasses: String,
});

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
