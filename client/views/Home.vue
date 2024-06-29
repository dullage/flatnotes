<template>
  <div class="flex h-full items-center justify-center">
    <div class="flex max-w-[500px] flex-1 flex-col items-center">
      <Logo class="mb-5" />
      <SearchInput class="mb-5 shadow-[0_0_20px] shadow-theme-shadow" />
      <LoadingIndicator
        :class="{ hidden: globalStore.hideRecentlyModified}"
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
      <LoadingIndicator
        :class="{ hidden: globalStore.hidePinnedNotes}"
        ref="pinnedLoadingIndicator"
        class="flex min-h-56 flex-col items-center"
        hideLoader
      >
        <p
          v-if="pinned.length > 0"
          class="mb-2 text-xs font-bold text-theme-text-very-muted"
        >
          PINNED
        </p>
        <RouterLink
          v-for="note in pinned"
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

import { mdiPencil, mdiPin } from "@mdi/js";
import { apiErrorHandler, getNotes } from "../api.js";
import CustomButton from "../components/CustomButton.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import Logo from "../components/Logo.vue";
import { useGlobalStore } from "../globalStore.js";
import SearchInput from "../partials/SearchInput.vue";

const globalStore = useGlobalStore();
const loadingIndicator = ref();
const pinnedLoadingIndicator = ref();
const noNotesMessage =
  "Click the 'New Note' button at the top of the page to get started.";
const noPinnedNotesMessage =
  "You can pin a note by adding #pinned anywhere in the content of a note.";
const notes = ref([]);
const pinned = ref([]);
const toast = useToast();

function init() {
  if (globalStore.hideRecentlyModified === false) {
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

  if (globalStore.hidePinnedNotes === false) {
    getNotes("tags:pinned", "lastModified", "desc", 5)
      .then((data) => {
        pinned.value = data;
        if (pinned.value.length > 0) {
          pinnedLoadingIndicator.value.setLoaded();
        } else {
          pinnedLoadingIndicator.value.setFailed(noPinnedNotesMessage, mdiPin);
        }
      })
      .catch((error) => {
        pinnedLoadingIndicator.value.setFailed();
        apiErrorHandler(error, toast);
      });
  }
}

// Watch to allow for delayed config load.
watch(() => globalStore.hideRecentlyModified, init);
onMounted(init);
</script>
