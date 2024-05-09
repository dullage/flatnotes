<template>
  <Modal v-model="isVisible">
    <SearchInput
      class="px-5 py-4 border-none"
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
