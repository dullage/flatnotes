<template>
  <Modal
    v-model="isVisible"
    :title="title"
    :closeHandler="emitClose"
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
        @click="emitClose('cancel')"
        class="mr-2"
      />
      <CustomButton
        v-if="rejectButtonText"
        :label="rejectButtonText"
        :style="rejectButtonStyle"
        @click="emitClose('reject')"
        class="mr-2"
      />
      <CustomButton
        v-focus
        :label="confirmButtonText"
        :style="confirmButtonStyle"
        @click="emitClose('confirm')"
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
  rejectButtonStyle: { type: String, default: "danger" },
  rejectButtonText: { type: String },
});
const emit = defineEmits(["confirm", "reject", "cancel"]);
const isVisible = defineModel({ type: Boolean });

function emitClose(closeEvent = "cancel") {
  isVisible.value = false;
  emit(closeEvent);
}
</script>
