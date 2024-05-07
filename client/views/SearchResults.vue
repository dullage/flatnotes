<template>
  <div class="flex h-full flex-col">
    <!-- Search Input -->
    <SearchInput
      :initialSearchTerm="props.searchTerm"
      class="mb-8 max-w-[700px]"
    />

    <!-- Search Results -->
    <LoadingIndicator ref="loadingIndicator" class="max-w-[700px] flex-1">
      <div
        v-for="result in results"
        class="mb-4 cursor-pointer rounded px-2 py-1 hover:bg-theme-background-elevated"
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
    </LoadingIndicator>
  </div>
</template>

<script setup>
import { useToast } from "primevue/usetoast";
import { onMounted, ref, watch } from "vue";

import { mdiMagnify } from "@mdi/js";
import { getNotes } from "../api.js";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import Tag from "../components/Tag.vue";
import { getUnknownServerErrorToastOptions } from "../helpers.js";
import SearchInput from "../partials/SearchInput.vue";

const props = defineProps({ searchTerm: String });

const loadingIndicator = ref();
const results = ref([]);
const toast = useToast();

function init() {
  loadingIndicator.value.setLoading();
  getNotes(props.searchTerm)
    .then((data) => {
      results.value = data;
      if (results.value.length > 0) {
        loadingIndicator.value.setLoaded();
      } else {
        loadingIndicator.value.setFailed("No Results", mdiMagnify);
      }
    })
    .catch(() => {
      loadingIndicator.value.setFailed();
      toast.add(getUnknownServerErrorToastOptions());
    });
}

watch(() => props.searchTerm, init);
onMounted(init);
</script>

<style>
.match {
  @apply text-theme-brand;
}
</style>
