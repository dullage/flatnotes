<template>
  <Modal ref="modal" class="flex flex-col items-center">
    <Logo class="mb-4" />
    <SearchInput @search="toggle" />
  </Modal>
</template>

<script setup>
import { ref } from "vue";

import Modal from "../components/Modal.vue";
import SearchInput from "./SearchInput.vue";
import Logo from "../components/Logo.vue";

const modal = ref();

function toggle() {
  modal.value.toggle();
}

defineExpose({ toggle });
</script>
