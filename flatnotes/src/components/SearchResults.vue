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
      <button type="button" class="bttn mb-3" @click="toggleHighlights">
        <b-icon :icon="showHighlights ? 'eye-slash' : 'eye'"></b-icon>
        {{ showHighlights ? "Hide" : "Show" }} Highlights
      </button>
      <div
        v-for="result in searchResults"
        :key="result.title"
        class="bttn result mb-2"
      >
        <a :href="result.href" @click.prevent="openNote(result.href)">
          <div class="d-flex align-items-center">
            <p
              class="result-title"
              v-html="
                showHighlights ? result.titleHighlightsOrTitle : result.title
              "
            ></p>
          </div>
          <p
            v-show="showHighlights"
            class="result-contents"
            v-html="result.contentHighlights"
          ></p>
          <div v-show="showHighlights">
            <span v-for="tag in result.tagMatches" :key="tag" class="tag mr-2"
              >#{{ tag }}</span
            >
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

.result p {
  margin: 0;
}

.result-title {
  color: $text;
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

.tag {
  color: white;
  font-size: 14px;
  background-color: $logo-key-colour;
  padding: 2px 6px;
  border-radius: 4px;
}
</style>

<script>
import * as constants from "../constants";
import * as helpers from "../helpers";

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
      showHighlights: true,
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
                  result.contentHighlights,
                  result.tagMatches
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

    toggleHighlights: function () {
      this.showHighlights = !this.showHighlights;
      helpers.setSearchParam(
        constants.params.showHighlights,
        this.showHighlights
      );
    },

    init: function () {
      this.getSearchResults();
    },
  },

  created: function () {
    this.init();

    let showHighlightsParam = helpers.getSearchParam(
      constants.params.showHighlights
    );
    if (typeof showHighlightsParam == "string") {
      this.showHighlights = showHighlightsParam === "true";
    } else {
      this.showHighlights = true;
    }
  },
};
</script>
