<template>
  <Modal v-model="isVisible" title="Search">
    <SearchInput @search="toggleHandler" class="mb-4" hidePlaceholder />
    <div class="flex justify-end">
      <CustomButton label="Close" @click="toggleHandler" />
    </div>
  </Modal>
</template>

<script setup>
import CustomButton from "../components/CustomButton.vue";
import Modal from "../components/Modal.vue";
import SearchInput from "./SearchInput.vue";

const isVisible = defineModel({ type: Boolean });

function toggleHandler() {
  isVisible.value = !isVisible.value;
}
</script>
