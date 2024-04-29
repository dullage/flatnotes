<template>
  <form class="flex w-full max-w-[500px]" @submit.prevent="search">
    <TextInput v-model="searchTerm" placeholder="Search" class="rounded-r-none" />
    <CustomButton
      :iconPath="mdilMagnify"
      iconSize="1.75em"
      class="rounded-l-none border border-l-0 border-theme-border focus:outline-none focus:ring-1"
    />
  </form>
</template>

<script setup>
import { mdilMagnify } from "@mdi/light-js";
import { useRouter } from "vue-router";
import { ref } from "vue";
import * as constants from "../constants";

import CustomButton from "../components/CustomButton.vue";
import TextInput from "../components/TextInput.vue";

const router = useRouter();
const searchTerm = ref("");

function search() {
  router.push({
    name: "search",
    query: { [constants.params.searchTerm]: searchTerm.value },
  });
}
</script>
