<template>
  <form
    class="flex w-full rounded-md border border-theme-border bg-theme-background px-3 py-2 dark:bg-theme-background-elevated"
    @submit.prevent="search"
  >
    <IconLabel :iconPath="mdilMagnify" class="mr-2" />
    <input
      type="text"
      v-model="searchTerm"
      v-focus
      class="w-full focus:outline-none bg-theme-background-elevated"
      placeholder="Search..."
    />
  </form>
</template>

<script setup>
import { mdilMagnify } from "@mdi/light-js";
import { useToast } from "primevue/usetoast";
import { ref } from "vue";
import { useRouter } from "vue-router";
import * as constants from "../constants";

import IconLabel from "../components/IconLabel.vue";
import { getToastOptions } from "../helpers.js";

const props = defineProps({
  initialSearchTerm: String,
});
const emit = defineEmits(["search"]);

const router = useRouter();
const searchTerm = ref(props.initialSearchTerm);
const toast = useToast();

function search() {
  if (searchTerm.value) {
    router.push({
      name: "search",
      query: { [constants.params.searchTerm]: searchTerm.value },
    });
    emit("search");
  } else {
    toast.add(getToastOptions("Error", "Please enter a search term.", true));
  }
}
</script>
