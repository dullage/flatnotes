<template>
  <div>
    <!-- Searching -->
    <div
      v-if="searchResults == null || searchResults.length == 0"
      class="h-100 d-flex flex-column justify-content-center"
    >
      <LoadingIndicator
        :failed="searchFailed"
        :failedBootstrapIcon="searchFailedIcon"
        :failedMessage="searchFailedMessage"
      />
    </div>

    <!-- Search Results Loaded -->
    <div v-else>
      <div v-for="result in searchResults" :key="result.title" class="mb-4">
        <p class="font-weight-bold mb-0">
          <a
            v-html="result.titleHighlightsOrTitle"
            :href="result.href"
            @click.prevent="openNote(result.href)"
          ></a>
        </p>
        <p class="result-contents" v-html="result.contentHighlights"></p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

a {
  &:hover {
    filter: opacity(70%);
  }
}

.result-contents {
  color: $muted-text;
}
</style>

<style lang="scss">
@import "../colours";

.match {
  font-weight: bold;
  color: $logo-key-colour;
}
</style>

<script>
import EventBus from "../eventBus";
import LoadingIndicator from "./LoadingIndicator";
import { SearchResult } from "../classes";
import api from "../api";

export default {
  components: {
    LoadingIndicator,
  },

  props: {
    searchTerm: { type: String, required: true },
  },

  data: function () {
    return {
      searchFailed: false,
      searchFailedMessage: "Failed to load Search Results",
      searchFailedIcon: null,
      searchResults: null,
    };
  },

  watch: {
    searchTerm: function () {
      this.init();
    },
  },

  methods: {
    getSearchResults: function () {
      let parent = this;
      this.searchFailed = false;
      api
        .get("/api/search", { params: { term: this.searchTerm } })
        .then(function (response) {
          parent.searchResults = [];
          if (response.data.length == 0) {
            parent.searchFailedIcon = "search";
            parent.searchFailedMessage = "No Results";
            parent.searchFailed = true;
          } else {
            response.data.forEach(function (result) {
              parent.searchResults.push(
                new SearchResult(
                  result.title,
                  result.lastModified,
                  result.titleHighlights,
                  result.contentHighlights
                )
              );
            });
          }
        })
        .catch(function (error) {
          if (!error.handled) {
            parent.searchFailed = true;
            EventBus.$emit("unhandledServerError");
          }
        });
    },

    openNote: function (href) {
      EventBus.$emit("navigate", href);
    },

    init: function () {
      this.getSearchResults();
    },
  },

  created: function () {
    this.init();
  },
};
</script>
