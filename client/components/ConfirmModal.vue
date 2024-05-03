<template>
  <!-- Mask -->
  <div
    class="fixed left-0 top-0 z-50 flex h-dvh w-dvw items-center justify-center bg-theme-background-tint/40 backdrop-blur-sm"
    :class="{ hidden: !isVisible }"
  >
    <!-- Modal -->
    <div
      class="max-w-96 grow rounded-lg border border-theme-border bg-theme-background px-6 py-4 shadow-lg"
      :class="{ 'border border-l-4 border-l-theme-failure': isDanger }"
    >
      <!-- Title -->
      <div class="mb-6 text-xl">{{ title }}</div>
      <!-- Message -->
      <div class="mb-6">{{ message }}</div>
      <!-- Buttons -->
      <div class="flex justify-end">
        <CustomButton label="Cancel" @click="cancelHandler" class="mr-2" />
        <CustomButton label="Confirm" @click="confirmHandler" isCta />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import CustomButton from "./CustomButton.vue";

const props = defineProps({
  title: { type: String, default: "Confirmation" },
  message: String,
  isDanger: Boolean,
});
const emit = defineEmits(["confirm", "cancel"]);

const isVisible = ref(false);

function toggle() {
  isVisible.value = !isVisible.value;
}

function cancelHandler() {
  isVisible.value = false;
  emit("cancel");
}

function confirmHandler() {
  isVisible.value = false;
  emit("confirm");
}

defineExpose({ toggle });
</script>
