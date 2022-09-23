<template>
  <div class="mb-4">
    <!-- Input -->
    <SearchInput :initial-value="searchTerm" class="mb-1"></SearchInput>

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
      <!-- Controls -->
      <div class="mb-3">
        <select v-model="sortBy" class="bttn sort-select">
          <option
            v-for="option in sortOptions"
            :key="option"
            :value="option"
            class="p-0"
          >
            Order: {{ sortOptionToString(option) }}
          </option>
        </select>

        <button
          v-if="searchResultsIncludeHighlights"
          type="button"
          class="bttn"
          @click="showHighlights = !showHighlights"
        >
          <b-icon :icon="showHighlights ? 'eye-slash' : 'eye'"></b-icon>
          {{ showHighlights ? "Hide" : "Show" }} Highlights
        </button>
      </div>

      <!-- Results -->
      <div
        v-for="group in resultsGrouped"
        :key="group.name"
        :class="{ 'mb-5': sortByIsGrouped }"
      >
        <p v-if="sortByIsGrouped" class="group-name">{{ group.name }}</p>
        <div
          v-for="result in group.searchResults"
          :key="result.title"
          class="bttn result"
          :class="{ 'mb-3': searchResultsIncludeHighlights && showHighlights }"
        >
          <a :href="result.href" @click.prevent="openNote(result.href)">
            <div class="d-flex justify-content-between">
              <p
                class="result-title"
                v-html="
                  showHighlights ? result.titleHighlightsOrTitle : result.title
                "
              ></p>
              <span
                class="last-modified"
                v-b-tooltip.hover
                title="Last Modified"
              >
                {{ result.lastModifiedAsString }}
              </span>
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
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

.sort-select {
  padding-inline: 6px;
}

.group-name {
  padding-left: 8px;
  font-weight: bold;
  font-size: 32px;
  color: $very-muted-text;
  margin-bottom: 8px;
}

.result p {
  margin: 0;
}

.result-title {
  color: $text;
}

.last-modified {
  color: $muted-text;
  font-size: 12px;
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
import SearchInput from "./SearchInput";
import { SearchResult } from "../classes";
import api from "../api";

export default {
  components: {
    LoadingIndicator,
    SearchInput,
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
      searchResultsIncludeHighlights: null,
      sortBy: 0,
      showHighlights: true,
    };
  },

  computed: {
    sortByIsGrouped: function () {
      return this.sortBy == this.sortOptions.title;
    },

    resultsGrouped: function () {
      if (this.sortBy == this.sortOptions.title) {
        return this.resultsByTitle();
      } else if (this.sortBy == this.sortOptions.lastModified) {
        return this.resultsByLastModified();
      } else {
        // Default
        return this.resultsByScore();
      }
    },
  },

  watch: {
    searchTerm: function () {
      this.init();
    },

    sortBy: function () {
      helpers.setSearchParam(constants.params.sortBy, this.sortBy);
    },

    showHighlights: function () {
      helpers.setSearchParam(
        constants.params.showHighlights,
        this.showHighlights
      );
    },
  },

  methods: {
    getSearchResults: function () {
      let parent = this;
      this.searchFailed = false;
      this.searchResultsIncludeHighlights = false;
      api
        .get("/api/search", { params: { term: this.searchTerm } })
        .then(function (response) {
          parent.searchResults = [];
          if (response.data.length == 0) {
            parent.searchFailedIcon = "search";
            parent.searchFailedMessage = "No Results";
            parent.searchFailed = true;
          } else {
            response.data.forEach(function (responseItem) {
              let searchResult = new SearchResult(responseItem);
              parent.searchResults.push(searchResult);
              if (
                parent.searchResultsIncludeHighlights == false &&
                searchResult.includesHighlights
              ) {
                parent.searchResultsIncludeHighlights = true;
              }
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

    resultsByScore: function () {
      return [
        {
          name: "_",
          searchResults: [...this.searchResults].sort(function (
            searchResultA,
            searchResultB
          ) {
            return searchResultB.score - searchResultA.score;
          }),
        },
      ];
    },

    resultsByLastModified: function () {
      return [
        {
          name: "_",
          searchResults: this.searchResults.sort(function (
            searchResultA,
            searchResultB
          ) {
            return searchResultB.lastModified - searchResultA.lastModified;
          }),
        },
      ];
    },

    resultsByTitle: function () {
      // Set up an empty dictionary of groups
      let notesGroupedDict = {};
      let specialCharGroupTitle = "#";
      [specialCharGroupTitle, ...constants.alphabet].forEach(function (group) {
        notesGroupedDict[group] = [];
      });

      // Add results to the group dictionary
      this.searchResults.forEach(function (searchResult) {
        let firstCharUpper = searchResult.title[0].toUpperCase();
        if (constants.alphabet.includes(firstCharUpper)) {
          notesGroupedDict[firstCharUpper].push(searchResult);
        } else {
          notesGroupedDict[specialCharGroupTitle].push(searchResult);
        }
      });

      // Convert dict to an array skipping empty groups
      let notesGroupedArray = [];
      Object.entries(notesGroupedDict).forEach(function (item) {
        if (item[1].length) {
          notesGroupedArray.push({
            name: item[0],
            searchResults: item[1].sort(function (
              SearchResultA,
              SearchResultB
            ) {
              // Sort by title within each group
              return SearchResultA.title.localeCompare(SearchResultB.title);
            }),
          });
        }
      });

      // Ensure the array is ordered correctly
      notesGroupedArray.sort(function (groupA, groupB) {
        return groupA.name.localeCompare(groupB.name);
      });

      return notesGroupedArray;
    },

    openNote: function (href) {
      EventBus.$emit("navigate", href);
    },

    sortOptionToString: function (sortOption) {
      let sortOptionStrings = {
        0: "Score",
        1: "Title",
        2: "Last Modified",
      };
      return sortOptionStrings[sortOption];
    },

    init: function () {
      this.sortBy = helpers.getSearchParamInt(constants.params.sortBy, 0);

      this.showHighlights = helpers.getSearchParamBool(
        constants.params.showHighlights,
        true
      );

      this.getSearchResults();
    },
  },

  created: function () {
    this.sortOptions = constants.searchSortOptions;
    this.init();
  },
};
</script>
