<template>
  <Modal
    ref="modal"
    :title="title"
    :class="{ 'border border-l-4 border-l-theme-danger': isDanger }"
    :closeHandler="cancelHandler"
  >
    <!-- Message -->
    <div class="mb-6">{{ message }}</div>
    <!-- Buttons -->
    <div class="flex justify-end">
      <CustomButton label="Cancel" @click="cancelHandler" class="mr-2" />
      <CustomButton :label="confirmButtonText" @click="confirmHandler" danger />
    </div>
  </Modal>
</template>

<script setup>
import { ref } from "vue";

import CustomButton from "./CustomButton.vue";
import Modal from "./Modal.vue";

const props = defineProps({
  title: { type: String, default: "Confirmation" },
  message: String,
  confirmButtonText: { type: String, default: "Confirm" },
  isDanger: Boolean,
});
const emit = defineEmits(["confirm", "cancel"]);

const modal = ref();

function toggle() {
  modal.value.toggle();
}

function cancelHandler() {
  modal.value.setVisibility(false);
  emit("cancel");
}

function confirmHandler() {
  modal.value.setVisibility(false);
  emit("confirm");
}

defineExpose({ toggle });
</script>
