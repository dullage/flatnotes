<template>
  <Modal ref="modal" title="Search">
    <SearchInput @search="toggle" class="mb-4" hidePlaceholder />
    <div class="flex justify-end">
      <CustomButton label="Close" @click="toggle" />
    </div>
  </Modal>
</template>

<script setup>
import { ref } from "vue";

import CustomButton from "../components/CustomButton.vue";
import Modal from "../components/Modal.vue";
import SearchInput from "./SearchInput.vue";

const modal = ref();

function toggle() {
  modal.value.toggle();
}

defineExpose({ toggle });
</script>
