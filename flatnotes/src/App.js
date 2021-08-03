import axios from "axios";
import { Note, SearchResult } from "./classes";

export default {
  data: function() {
    return {
      notes: [],
      searchTerm: null,
      searchTimeout: null,
      searchResults: [],
    };
  },

  computed: {
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
        this.searchResults = [];
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
  },

  created: function() {
    this.getNotes();
  },
};
