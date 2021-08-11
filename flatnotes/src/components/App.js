import "@toast-ui/editor/dist/toastui-editor.css";
import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Editor } from "@toast-ui/vue-editor";
import { Viewer } from "@toast-ui/vue-editor";
import axios from "axios";

import { Note, SearchResult } from "./classes";

export default {
  components: {
    Viewer,
    Editor,
  },

  data: function() {
    return {
      notes: [],
      searchTerm: null,
      searchTimeout: null,
      searchResults: null,
      currentNote: null,
      editMode: false,
    };
  },

  computed: {
    currentView: function() {
      // 3 - Edit Note
      if (this.currentNote && this.editMode) {
        return 3;
      }
      // 2 - View Note
      else if (this.currentNote) {
        return 2;
      }
      // 1 - Search Results
      else if (this.searchResults) {
        return 1;
      }
      // 0 - Notes List
      else {
        return 0;
      }
    },

    notesByLastModifiedDesc: function() {
      return this.notes.sort(function(a, b) {
        return b.lastModified - a.lastModified;
      });
    },
  },

  watch: {
    searchTerm: function() {
      this.clearSearchTimeout();
      if (this.searchTerm) {
        this.startSearchTimeout();
      } else {
        this.searchResults = null;
      }
    },
  },

  methods: {
    getNotes: function() {
      parent = this;
      parent.notes = [];
      axios.get("/api/notes").then(function(response) {
        response.data.forEach(function(note) {
          parent.notes.push(new Note(note.filename, note.lastModified));
        });
      });
    },

    clearSearchTimeout: function(params) {
      if (this.searchTimeout != null) {
        clearTimeout(this.searchTimeout);
      }
    },

    startSearchTimeout: function() {
      this.clearSearchTimeout();
      this.searchTimeout = setTimeout(this.search, 1000);
    },

    search: function() {
      parent = this;
      this.clearSearchTimeout();
      this.searchResults = [];
      if (this.searchTerm) {
        axios
          .get("/api/search", { params: { term: this.searchTerm } })
          .then(function(response) {
            response.data.forEach(function(result) {
              parent.searchResults.push(
                new SearchResult(
                  result.filename,
                  result.lastModified,
                  result.titleHighlights,
                  result.contentHighlights
                )
              );
            });
          });
      }
    },

    loadNote: function(filename) {
      parent = this;
      axios.get(`/api/notes/${filename}`).then(function(response) {
        parent.currentNote = response.data;
      });
    },

    unloadNote: function() {
      this.currentNote = null;
      this.editMode = false;
    },

    saveNote: function() {
      parent = this;
      let newContent = this.$refs.toastUiEditor.invoke("getMarkdown");
      if (newContent != this.currentNote.content) {
        axios
          .patch(`/api/notes/${this.currentNote.filename}`, {
            newContent: newContent,
          })
          .then(function(response) {
            parent.currentNote = response.data;
            parent.editMode = false;
          });
      } else {
        this.editMode = false;
      }
    },
  },

  created: function() {
    this.getNotes();
  },
};
