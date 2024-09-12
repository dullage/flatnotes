<template>
  <div class="flex h-full items-center justify-center">
    <div class="flex max-w-[500px] flex-1 flex-col items-center">
      <Logo class="mb-5" />
      <SearchInput class="mb-5 shadow-[0_0_20px] shadow-theme-shadow" />
      <LoadingIndicator
        ref="loadingIndicator"
        class="flex min-h-56 flex-col items-center"
        hideLoader
      >
        <p
          v-if="notes.length > 0"
          class="mb-2 text-xs font-bold text-theme-text-very-muted"
        >
          RECENTLY MODIFIED
        </p>
        <RouterLink
          v-for="note in notes"
          :to="{ name: 'note', params: { title: note.title } }"
          class="mb-1"
        >
          <CustomButton :label="note.title" />
        </RouterLink>
      </LoadingIndicator>
    </div>
  </div>
</template>

<script setup>
import { useToast } from "primevue/usetoast";
import { onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";

import { mdiPencil } from "@mdi/js";
import { apiErrorHandler, getNotes } from "../api.js";
import CustomButton from "../components/CustomButton.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import Logo from "../components/Logo.vue";
import { useGlobalStore } from "../globalStore.js";
import SearchInput from "../partials/SearchInput.vue";

const globalStore = useGlobalStore();
const loadingIndicator = ref();
const noNotesMessage =
  "Click the 'New Note' button at the top of the page to get started.";
const notes = ref([]);
const toast = useToast();

function init() {
  if (globalStore.config.hideRecentlyModified) {
    return;
  }
  getNotes("*", "lastModified", "desc", 5)
    .then((data) => {
      notes.value = data;
      if (notes.value.length > 0) {
        loadingIndicator.value.setLoaded();
      } else {
        loadingIndicator.value.setFailed(noNotesMessage, mdiPencil);
      }
    })
    .catch((error) => {
      loadingIndicator.value.setFailed();
      apiErrorHandler(error, toast);
    });
}

// Watch to allow for delayed config load.
watch(() => globalStore.config.hideRecentlyModified, init);
onMounted(init);
</script>
