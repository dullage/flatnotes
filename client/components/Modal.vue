<template>
  <!-- Mask -->
  <div
    v-if="isVisible"
    class="fixed left-0 top-0 z-50 flex h-dvh w-dvw items-start justify-center bg-slate-950/40 backdrop-blur-sm"
    @click.self="closeHandler"
  >
    <!-- Modal -->
    <div
      class="relative mx-2 mt-[30vh] max-w-[500px] grow rounded-lg border border-theme-border bg-theme-background shadow-lg"
      :class="$attrs.class"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, watch } from "vue";
import Mousetrap from "mousetrap";

defineOptions({
  inheritAttrs: false,
});
const props = defineProps({
  closeHandlerOverride: Function,
});
const isVisible = defineModel({ type: Boolean });

// Make backgound inert when a modal is open
function setBackgroundInert(isInert) {
  document.querySelectorAll("[data-inert-scope]").forEach((el) => {
    if (isInert) {
      el.setAttribute("inert", "");
    } else {
      el.removeAttribute("inert");
    }
  });
}

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

watch(isVisible, (visible) => {
  if (visible) {
    setBackgroundInert(true);
  } else {
    setBackgroundInert(false);
  }
});

onBeforeUnmount(() => {
  setBackgroundInert(false);
});
</script>
