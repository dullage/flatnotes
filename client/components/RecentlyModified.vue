<template>
  <div>
    <!-- Loading -->
    <div
      v-if="notes == null || notes.length == 0"
      class="h-100 d-flex flex-column justify-content-center"
    >
      <LoadingIndicator
        :failed="loadingFailed"
        :failedMessage="loadingFailedMessage"
        :failedBootstrapIcon="loadingFailedIcon"
        :show-loader="false"
      />
    </div>

    <!-- Notes Loaded -->
    <div v-else class="d-flex flex-column align-items-center">
      <p class="mini-header mb-1">RECENTLY MODIFIED</p>
      <a
        v-for="note in notes"
        :key="note.title"
        class="bttn"
        :href="note.href"
        @click.prevent="openNote(note.href, $event)"
      >
        {{ note.title }}
      </a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

.mini-header {
  font-size: 0.75rem;
  font-weight: bold;
  color: var(--colour-text-very-muted);
}
</style>

<script>
import EventBus from "../eventBus.js";
import LoadingIndicator from "./LoadingIndicator.vue";
import { SearchResult } from "../classes.js";
import api from "../api.js";

export default {
  components: {
    LoadingIndicator,
  },

  props: {
    maxNotes: { type: Number },
  },

  data: function () {
    return {
      notes: null,
      loadingFailed: false,
      loadingFailedMessage: "Failed to load notes",
      loadingFailedIcon: null,
    };
  },

  methods: {
    getNotes: function () {
      let parent = this;
      this.loadingFailed = false;
      api
        .get("/api/search", {
          params: {
            term: "*",
            sort: "lastModified",
            order: "desc",
            limit: this.maxNotes,
          },
        })
        .then(function (response) {
          parent.notes = [];
          if (response.data.length) {
            response.data.forEach(function (searchResult) {
              parent.notes.push(new SearchResult(searchResult));
            });
          } else {
            parent.loadingFailedMessage =
              "Click the 'New' button at the top of the page to add your first note";
            parent.loadingFailedIcon = "pencil";
            parent.loadingFailed = true;
          }
        })
        .catch(function (error) {
          parent.loadingFailed = true;
          if (!error.handled) {
            EventBus.$emit("unhandledServerErrorToast");
          }
        });
    },

    openNote: function (href, event) {
      EventBus.$emit("navigate", href, event);
    },
  },

  created: function () {
    this.getNotes();
  },
};
</script>
