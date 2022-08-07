<template>
  <form v-on:submit.prevent="search" class="w-100">
    <div class="input-group w-100">
      <input
        id="search-input"
        type="text"
        class="form-control"
        :class="{ highlight: includeHighlightClass }"
        placeholder="Search"
        v-model="searchTermInput"
      />
      <div class="input-group-append">
        <button class="btn" type="submit">
          <b-icon icon="search"></b-icon>
        </button>
      </div>
    </div>
  </form>
</template>

<style lang="scss" scoped>
@keyframes highlight {
  from {
    background-color: #bbcdff;
  }
  to {
    background-color: white;
  }
}

.highlight {
  animation-name: highlight;
  animation-duration: 1.5s;
}

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

export default {
  data: function () {
    return {
      searchTermInput: null,
      includeHighlightClass: false,
    };
  },

  methods: {
    search: function () {
      if (this.searchTermInput) {
        this.searchTermInput = this.searchTermInput.trim();
      }
      if (this.searchTermInput) {
        EventBus.$emit(
          "navigate",
          `/${constants.basePaths.search}?${
            constants.params.searchTerm
          }=${encodeURI(this.searchTermInput)}`
        );
      } else {
        this.$bvToast.toast("Please enter a search term ✘", {
          variant: "danger",
          noCloseButton: true,
        });
      }
    },

    highlightSearchInput: function () {
      let parent = this;
      this.includeHighlightClass = true;
      setTimeout(function () {
        parent.includeHighlightClass = false;
      }, 1500);
    },
  },

  created: function () {
    EventBus.$on("highlight-search-input", this.highlightSearchInput);
  },
};
</script>
