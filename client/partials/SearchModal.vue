<template>
  <Modal v-model="isVisible" class="px-0 py-0 border-none">
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
