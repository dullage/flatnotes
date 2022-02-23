import "@toast-ui/editor/dist/toastui-editor.css";
import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Editor } from "@toast-ui/vue-editor";
import { Viewer } from "@toast-ui/vue-editor";

import api from "../api";
import * as constants from "../constants";
import { Note, SearchResult } from "./classes";
import EventBus from "../eventBus";
import * as helpers from "../helpers";

export default {
  components: {
    Viewer,
    Editor,
  },

  data: function() {
    return {
      views: {
        login: 0,
        home: 1,
        note: 2,
        search: 3,
      },
      currentView: 1,
      usernameInput: null,
      passwordInput: null,
      rememberMeInput: false,
      notes: [],
      searchTerm: null,
      draftSaveTimeout: null,
      searchResults: null,
      currentNote: null,
      titleInput: null,
      initialContent: null,
      editMode: false,
    };
  },

  computed: {
    notesByLastModifiedDesc: function() {
      return this.notes.sort(function(a, b) {
        return b.lastModified - a.lastModified;
      });
    },
  },

  methods: {
    route: function() {
      let path = window.location.pathname.split("/");
      let basePath = path[1];

      // Home Page
      if (basePath == "") {
        this.getNotes();
        this.currentView = this.views.home;
      }

      // Search
      else if (basePath == constants.basePaths.search) {
        this.searchTerm = helpers.getSearchParam(constants.params.searchTerm);
        this.getSearchResults();
        this.currentView = this.views.search;
      }

      // Note
      else if (basePath == constants.basePaths.note) {
        let noteTitle = path[2];
        this.loadNote(noteTitle);
        this.currentView = this.views.note;
      }

      // Login
      else if (basePath == constants.basePaths.login) {
        this.currentView = this.views.login;
      }

      this.updateDocumentTitle();
    },

    updateDocumentTitle: function() {
      let pageTitleSuffix = null;
      if (this.currentView == this.views.login) {
        pageTitleSuffix = "Login";
      } else if (this.currentView == this.views.search) {
        pageTitleSuffix = "Search";
      } else if (
        this.currentView == this.views.note &&
        this.currentNote != null
      ) {
        pageTitleSuffix = this.currentNote.title;
      }
      window.document.title =
        (pageTitleSuffix ? `${pageTitleSuffix} - ` : "") + "flatnotes";
    },

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
          let redirectPath = helpers.getSearchParam(constants.params.redirect);
          window.open(redirectPath || "/", "_self");
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
      window.open(`/${constants.basePaths.login}`, "_self");
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

    search: function() {
      window.open(
        `/${constants.basePaths.search}?${
          constants.params.searchTerm
        }=${encodeURI(this.searchTerm)}`,
        "_self"
      );
    },

    getSearchResults: function() {
      var parent = this;
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
    },

    getContentForEditor: function() {
      let draftContent = localStorage.getItem(this.currentNote.filename);
      if (draftContent) {
        if (confirm("Do you want to resume the saved draft?")) {
          return draftContent;
        } else {
          localStorage.removeItem(this.currentNote.filename);
        }
      }
      return this.currentNote.content;
    },

    loadNote: function(filename) {
      let parent = this;
      api
        .get(`/api/notes/${filename}.${constants.markdownExt}`)
        .then(function(response) {
          parent.currentNote = new Note(
            response.data.filename,
            response.data.lastModified,
            response.data.content
          );
          parent.updateDocumentTitle();
        });
    },

    toggleEditMode: function() {
      // To Edit Mode
      if (this.editMode == false) {
        this.titleInput = this.currentNote.title;
        let draftContent = localStorage.getItem(this.currentNote.filename);
        // Draft
        if (draftContent && confirm("Do you want to resume the saved draft?")) {
          this.initialContent = draftContent;
        }
        // Non-Draft
        else {
          localStorage.removeItem(this.currentNote.filename);
          this.initialContent = this.currentNote.content;
        }
      }
      // To View Mode
      else {
        this.titleInput = null;
        this.initialContent = null;
      }
      // Always
      this.editMode = !this.editMode;
    },

    newNote: function() {
      this.currentNote = new Note();
      this.toggleEditMode();
      this.currentView = this.views.note;
    },

    getEditorContent: function() {
      return this.$refs.toastUiEditor.invoke("getMarkdown");
    },

    clearDraftSaveTimeout: function() {
      if (this.draftSaveTimeout != null) {
        clearTimeout(this.draftSaveTimeout);
      }
    },

    startDraftSaveTimeout: function() {
      this.clearDraftSaveTimeout();
      this.draftSaveTimeout = setTimeout(this.saveDraft, 1000);
    },

    saveDraft: function() {
      localStorage.setItem(this.currentNote.filename, this.getEditorContent());
    },

    saveNote: function() {
      let newContent = this.getEditorContent();

      // New Note
      if (this.currentNote.lastModified == null) {
        api
          .post(`/api/notes`, {
            filename: `${this.titleInput}.${constants.markdownExt}`,
            content: newContent,
          })
          .then(this.saveNoteResponseHandler);
      }

      // Modified Note
      else if (
        newContent != this.currentNote.content ||
        this.titleInput != this.currentNote.title
      ) {
        api
          .patch(`/api/notes/${this.currentNote.filename}`, {
            newFilename: `${this.titleInput}.${this.currentNote.ext}`,
            newContent: newContent,
          })
          .then(this.saveNoteResponseHandler);
      }

      // No Change
      else {
        this.toggleEditMode();
      }
    },

    saveNoteResponseHandler: function(response) {
      localStorage.removeItem(this.currentNote.filename);
      this.currentNote = new Note(
        response.data.filename,
        response.data.lastModified,
        response.data.content
      );
      this.updateDocumentTitle();
      history.replaceState(null, "", this.currentNote.href);
      this.toggleEditMode();
    },

    cancelNote: function() {
      localStorage.removeItem(this.currentNote.filename);
      if (this.currentNote.lastModified == null) {
        // Cancelling a new note
        this.currentNote = null;
        this.currentView = this.views.home;
      }
      this.toggleEditMode();
    },

    deleteNote: function() {
      if (
        confirm(
          `Are you sure you want to delete the note '${this.currentNote.title}'?`
        )
      ) {
        api
          .delete(`/api/notes/${this.currentNote.filename}`)
          .then(window.open("/", "_self"));
      }
    },

    keyboardShortcuts: function(e) {
      // 'e' to Edit
      if (
        e.key == "e" &&
        this.currentView == this.views.note &&
        this.editMode == false
      ) {
        e.preventDefault();
        this.toggleEditMode();
      }

      // 'CTRL + s' to Save
      // else if (
      //   e.key == "s" &&
      //   e.ctrlKey == true &&
      //   this.currentView == this.views.note &&
      //   this.editMode == true
      // ) {
      //   e.preventDefault();
      //   this.saveNote();
      // }
    },
  },

  created: function() {
    EventBus.$on("logout", this.logout);
    document.addEventListener("keydown", this.keyboardShortcuts);

    let token = localStorage.getItem("token");
    if (token != null) {
      sessionStorage.setItem("token", token);
    }

    this.route();
  },
};
