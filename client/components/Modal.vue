<template>
  <!-- Mask -->
  <div
    v-if="isVisible"
    class="fixed left-0 top-0 z-50 flex h-dvh w-dvw items-center justify-center bg-slate-950/40 backdrop-blur-sm"
    @click.self="closeHandler"
  >
    <!-- Modal -->
    <div
      class="relative max-w-[500px] grow rounded-lg border border-theme-border bg-theme-background px-6 py-4 shadow-lg"
      :class="$attrs.class"
      @keyup.esc="close"
    >
      <CustomButton
        v-if="props.showClose"
        :iconPath="mdiWindowClose"
        @click="closeHandler"
        class="absolute right-1 top-1"
      />
      <!-- Title -->
      <div v-if="title" class="mb-6 text-xl">{{ title }}</div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { mdiWindowClose } from "@mdi/js";
import Mousetrap from "mousetrap";

import CustomButton from "./CustomButton.vue";

defineOptions({
  inheritAttrs: false,
});
const props = defineProps({
  title: { type: String },
  showClose: { type: Boolean },
  closeHandlerOverride: Function,
});
const isVisible = defineModel({ type: Boolean });

// 'escape' to close
Mousetrap.bind("esc", () => {
  if (isVisible.value) {
    closeHandler();
  }
});

function closeHandler() {
  if (props.closeHandlerOverride) {
    props.closeHandlerOverride();
  } else {
    isVisible.value = false;
  }
}
</script>
