<template>
  <form v-on:submit.prevent="search" class="w-100">
    <div class="input-group w-100">
      <input
        type="text"
        class="form-control"
        placeholder="Search"
        v-model="searchTermInput"
        autofocus
      />
      <div class="input-group-append">
        <button class="btn" type="submit">
          <BIconSearch />
        </button>
      </div>
    </div>
  </form>
</template>

<style lang="scss" scoped>
.btn {
  border: 1px solid #cfd4da;
  svg {
    color: #a7abb1;
  }
}
</style>

<script>
import EventBus from "../eventBus";
import * as constants from "../constants";
import { BIconSearch } from "bootstrap-vue";

export default {
  comments: {
    BIconSearch,
  },

  data: function () {
    return {
      searchTermInput: null,
    };
  },

  methods: {
    search: function () {
      EventBus.$emit(
        "navigate",
        `/${constants.basePaths.search}?${
          constants.params.searchTerm
        }=${encodeURI(this.searchTermInput)}`
      );
    },
  },
};
</script>
