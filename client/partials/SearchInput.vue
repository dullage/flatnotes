<template>
  <form class="flex w-full" @submit.prevent="search">
    <TextInput
      v-model="searchTerm"
      v-focus
      :placeholder="props.hidePlaceholder ? '' : 'Search'"
      class="rounded-r-none"
    />
    <CustomButton
      :iconPath="mdilMagnify"
      iconSize="1.75em"
      class="rounded-l-none border border-l-0 border-theme-border focus:outline-none focus:ring-1"
    />
  </form>
</template>

<script setup>
import { mdilMagnify } from "@mdi/light-js";
import { useToast } from "primevue/usetoast";
import { ref } from "vue";
import { useRouter } from "vue-router";
import * as constants from "../constants";

import CustomButton from "../components/CustomButton.vue";
import TextInput from "../components/TextInput.vue";
import { getToastOptions } from "../helpers.js";

const props = defineProps({
  initialSearchTerm: String,
  hidePlaceholder: Boolean,
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
