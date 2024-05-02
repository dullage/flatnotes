<template>
  <div class="max-w-[700px]">
    <!-- Search Input -->
    <SearchInput :initialSearchTerm="props.searchTerm" class="mb-8" />

    <!-- Search Results -->
    <div
      v-for="result in results"
      class="mb-4 cursor-pointer rounded px-2 py-1 hover:bg-theme-background-tint dark:hover:bg-theme-background-elevated"
    >
      <RouterLink :to="result.href">
        <!-- Title and Tags -->
        <div>
          <span v-html="result.titleHighlightsOrTitle" class="mr-2"></span>
          <Tag v-for="tag in result.tagMatches" :tag="tag" class="mr-1" />
        </div>
        <!-- Last Modified and Content Highlights -->
        <div>
          <span class="text-theme-text-muted">{{
            result.lastModifiedAsString
          }}</span>
          <span v-if="result.contentHighlights"> - </span>
          <span
            v-html="result.contentHighlights"
            class="text-theme-text-muted"
          ></span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { useToast } from "primevue/usetoast";
import { ref, watch } from "vue";

import { getNotes } from "../api.js";
import { getUnknownServerErrorToastOptions } from "../helpers.js";
import SearchInput from "../partials/SearchInput.vue";
import Tag from "../components/Tag.vue";

const props = defineProps({ searchTerm: String });

const results = ref([]);
const toast = useToast();

function init() {
  getNotes(props.searchTerm)
    .then((data) => {
      results.value = data;
    })
    .catch(() => {
      toast.add(getUnknownServerErrorToastOptions());
    });
}

watch(() => props.searchTerm, init, { immediate: true });
</script>

<style>
.match {
  @apply text-theme-brand;
}
</style>
