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
        :show-loader="showLoader"
      />
    </div>

    <!-- Notes Loaded -->
    <div v-else>
      <p
        v-if="miniHeader"
        class="mini-header mb-1"
        :class="{ centered: centered }"
      >
        {{ miniHeader }}
      </p>
      <div
        v-for="group in notesGrouped"
        :key="group.name"
        :class="{ centered: centered, 'mb-5': grouped }"
      >
        <p v-if="grouped" class="group-name">{{ group.name }}</p>
        <a
          v-for="note in group.notes"
          :key="note.title"
          class="d-flex justify-content-between align-items-center note-row"
          :href="note.href"
          @click.prevent="openNote(note.href, $event)"
        >
          <span>{{ note.title }}</span>
          <span v-if="showLastModified" class="last-modified d-none d-md-block">
            {{ note.lastModifiedAsString }}
          </span>
        </a>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

.centered {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mini-header {
  text-transform: uppercase;
  font-size: 12px;
  font-weight: bold;
  color: $very-muted-text;
}

.group-name {
  padding-left: 8px;
  font-weight: bold;
  font-size: 32px;
  color: $very-muted-text;
}

.note-row {
  padding: 4px 8px;
  margin: 2px 0;
  border-radius: 4px;
  &:hover {
    background-color: $button-background;
  }
}

a {
  &:hover {
    filter: none;
    cursor: pointer;
  }
}

.last-modified {
  color: $muted-text;
  font-size: 12px;
}
</style>

<script>
import * as constants from "../constants";

import EventBus from "../eventBus";
import LoadingIndicator from "./LoadingIndicator.vue";
import { Note } from "../classes";
import api from "../api";

const alphaGroups = ["#", ...constants.alphabet];

export default {
  components: {
    LoadingIndicator,
  },

  props: {
    numRecentlyModified: { type: Number },
    grouped: { type: Boolean, default: false },
    showLastModified: { type: Boolean, default: false },
    centered: { type: Boolean, default: false },
    miniHeader: { type: String },
    showLoader: { type: Boolean, default: true },
  },

  data: function () {
    return {
      notes: null,
      loadingFailed: false,
      loadingFailedMessage: "Failed to load notes",
      loadingFailedIcon: null,
    };
  },

  computed: {
    notesGrouped: function () {
      if (!this.grouped) {
        return [{ name: "all", notes: this.notes }];
      }

      let notesGroupedDict = {};
      alphaGroups.forEach(function (group) {
        notesGroupedDict[group] = [];
      });

      this.notes.forEach(function (note) {
        let firstCharUpper = note.title[0].toUpperCase();
        if (constants.alphabet.includes(firstCharUpper)) {
          notesGroupedDict[firstCharUpper].push(note);
        } else {
          notesGroupedDict["#"].push(note);
        }
      });

      // Convert dict to an array skipping empty groups
      let notesGroupedArray = [];
      Object.entries(notesGroupedDict).forEach(function (item) {
        if (item[1].length) {
          notesGroupedArray.push({
            name: item[0],
            notes: item[1].sort(function (noteA, noteB) {
              return noteA.title.localeCompare(noteB.title);
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
  },

  methods: {
    getNotes: function () {
      let parent = this;
      api
        .get("/api/notes", {
          params: {
            limit: this.numRecentlyModified,
            sort: "lastModified",
            order: "desc",
          },
        })
        .then(function (response) {
          parent.notes = [];
          if (response.data.length) {
            response.data.forEach(function (note) {
              parent.notes.push(new Note(note.title, note.lastModified));
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
            EventBus.$emit("unhandledServerError");
          }
        });
    },

    notesByTitle: function () {
      return null;
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
