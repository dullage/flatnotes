<template>
  <Modal
    v-model="isVisible"
    :title="title"
    :class="{ 'border border-l-4 border-l-theme-danger': isDanger }"
    :closeHandler="cancelHandler"
    class="px-6 py-4"
  >
    <!-- Title -->
    <div v-if="title" class="mb-6 text-xl">{{ title }}</div>
    <!-- Message -->
    <div class="mb-6">{{ message }}</div>
    <!-- Buttons -->
    <div class="flex justify-end">
      <CustomButton
        :label="cancelButtonText"
        :style="cancelButtonStyle"
        @click="cancelHandler"
        class="mr-2"
      />
      <CustomButton
        v-focus
        :label="confirmButtonText"
        :style="confirmButtonStyle"
        @click="confirmHandler"
      />
    </div>
  </Modal>
</template>

<script setup>
import CustomButton from "./CustomButton.vue";
import Modal from "./Modal.vue";

const props = defineProps({
  title: { type: String, default: "Confirmation" },
  message: String,
  confirmButtonStyle: { type: String, default: "cta" },
  confirmButtonText: { type: String, default: "Confirm" },
  cancelButtonStyle: { type: String, default: "subtle" },
  cancelButtonText: { type: String, default: "Cancel" },
  isDanger: Boolean,
});
const emit = defineEmits(["confirm", "cancel"]);
const isVisible = defineModel({ type: Boolean });

function cancelHandler() {
  isVisible.value = false;
  emit("cancel");
}

function confirmHandler() {
  isVisible.value = false;
  emit("confirm");
}
</script>
