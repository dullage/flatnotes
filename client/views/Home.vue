<template>
  <div class="h-full">
    <div class="flex h-full flex-col items-center justify-center">
      <Logo class="mb-5" />
      <SearchInput class="mb-5 shadow-[0_0_20px] shadow-theme-shadow" />
      <div class="flex min-h-56 flex-col items-center">
        <p
          v-if="notes.length > 0"
          class="mb-2 text-xs font-bold text-theme-text-very-muted"
        >
          RECENTLY MODIFIED
        </p>
        <RouterLink v-for="note in notes" :to="note.href">
          <CustomButton :label="note.title" />
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import { getNotes } from "../api.js";
import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import SearchInput from "../partials/SearchInput.vue";
import { RouterLink } from "vue-router";

const notes = ref([]);

getNotes("*", "lastModified", "desc", 5).then((data) => {
  notes.value = data;
});
</script>
