import "@toast-ui/editor/dist/toastui-editor.css";
import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Editor } from "@toast-ui/vue-editor";
import { Viewer } from "@toast-ui/vue-editor";

import api from "../api";
import { Note, SearchResult } from "./classes";
import EventBus from "../eventBus";

export default {
  components: {
    Viewer,
    Editor,
  },

  data: function() {
    return {
      loggedIn: false,
      usernameInput: null,
      passwordInput: null,
      rememberMeInput: false,
      notes: [],
      searchTerm: null,
      searchTimeout: null,
      searchResults: null,
      currentNote: null,
      newFilename: null,
      editMode: false,
    };
  },

  computed: {
    currentView: function() {
      // 4 - Login
      if (this.loggedIn == false) {
        return 4;
      }
      // 3 - Edit Note
      else if (this.currentNote && this.editMode) {
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
    login: function() {
      let parent = this;
      api
        .post("/api/token", {
          username: this.usernameInput,
          password: this.passwordInput,
        })
        .then(function(response) {
          sessionStorage.setItem("token", response.data.access_token);
          if (parent.rememberMeInput == true) {
            localStorage.setItem("token", response.data.access_token);
          }
          parent.loggedIn = true;
          parent.getNotes();
        })
        .finally(function() {
          parent.usernameInput = null;
          parent.passwordInput = null;
          parent.rememberMeInput = false;
        });
    },

    logout: function() {
      sessionStorage.removeItem("token");
      localStorage.removeItem("token");
      this.loggedIn = false;
    },

    getNotes: function() {
      let parent = this;
      parent.notes = [];
      api.get("/api/notes").then(function(response) {
        response.data.forEach(function(note) {
          parent.notes.push(new Note(note.filename, note.lastModified));
        });
      });
    },

    clearSearchTimeout: function() {
      if (this.searchTimeout != null) {
        clearTimeout(this.searchTimeout);
      }
    },

    startSearchTimeout: function() {
      this.clearSearchTimeout();
      this.searchTimeout = setTimeout(this.search, 1000);
    },

    search: function() {
      let parent = this;
      this.clearSearchTimeout();
      if (this.searchTerm) {
        api
          .get("/api/search", { params: { term: this.searchTerm } })
          .then(function(response) {
            parent.searchResults = [];
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
      let parent = this;
      api.get(`/api/notes/${filename}`).then(function(response) {
        parent.currentNote = response.data;
        parent.newFilename = parent.currentNote.filename;
      });
    },

    newNote: function() {
      this.currentNote = new Note();
      this.editMode = true;
    },

    unloadNote: function() {
      this.currentNote = null;
      this.newFilename = null;
      this.editMode = false;
      this.getNotes();
    },

    saveNote: function() {
      let parent = this;
      let newContent = this.$refs.toastUiEditor.invoke("getMarkdown");

      // New Note
      if (this.currentNote.lastModified == null) {
        api
          .post(`/api/notes`, {
            filename: this.newFilename,
            content: newContent,
          })
          .then(function(response) {
            parent.currentNote = response.data;
            parent.newFilename = parent.currentNote.filename;
            parent.editMode = false;
          });
      }

      // Modified Note
      else if (
        newContent != this.currentNote.content ||
        this.newFilename != this.currentNote.filename
      ) {
        api
          .patch(`/api/notes/${this.currentNote.filename}`, {
            newFilename: this.newFilename,
            newContent: newContent,
          })
          .then(function(response) {
            parent.currentNote = response.data;
            parent.newFilename = parent.currentNote.filename;
            parent.editMode = false;
          });
      }

      // No Change
      else {
        this.editMode = false;
      }
    },
  },

  created: function() {
    EventBus.$on("logout", this.logout);

    let token = localStorage.getItem("token");
    if (token != null) {
      sessionStorage.setItem("token", token);
      this.loggedIn = true;
      this.getNotes();
    }
  },
};
