<template>
  <div class="flex h-full items-center justify-center">
    <div class="flex max-w-[500px] flex-1 flex-col items-center">
      <Logo class="mb-5" />
      <SearchInput class="mb-5 shadow-[0_0_20px] shadow-theme-shadow" />
      <div class="flex min-h-56 flex-col items-center">
        <p
          v-if="notes.length > 0"
          class="mb-2 text-xs font-bold text-theme-text-very-muted"
        >
          RECENTLY MODIFIED
        </p>
        <RouterLink v-for="note in notes" :to="note.href" class="mb-1">
          <CustomButton :label="note.title" />
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useToast } from "primevue/usetoast";
import { ref } from "vue";
import { RouterLink } from "vue-router";

import { getNotes, apiErrorHandler } from "../api.js";
import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import SearchInput from "../partials/SearchInput.vue";

const notes = ref([]);
const toast = useToast();

getNotes("*", "lastModified", "desc", 5)
  .then((data) => {
    notes.value = data;
  })
  .catch((error) => {
    apiErrorHandler(error, toast);
  });
</script>
