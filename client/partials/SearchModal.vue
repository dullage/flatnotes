<template>
  <Modal v-model="isVisible" class="border-none">
    <SearchInput
      class="px-5 py-4"
      @search="toggleHandler"
      @keyup.esc="toggleHandler"
    />
  </Modal>
</template>

<script setup>
import Modal from "../components/Modal.vue";
import SearchInput from "./SearchInput.vue";

const isVisible = defineModel({ type: Boolean });

function toggleHandler() {
  isVisible.value = !isVisible.value;
}
</script>
