<template>
  <Modal v-model="isVisible" class="border-none">
    <SearchInput
      large
      placeholder="Search by title, content or #tags..."
      @search="toggleHandler"
      @keydown.esc="toggleHandler"
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
