import { Editor } from "@toast-ui/vue-editor";
import { Viewer } from "@toast-ui/vue-editor";

import RecentlyModified from "./RecentlyModified";
import LoadingIndicator from "./LoadingIndicator";

import api from "../api";
import * as constants from "../constants";
import { Note, SearchResult } from "../classes";
import EventBus from "../eventBus";
import * as helpers from "../helpers";

export default {
  components: {
    Viewer,
    Editor,
    RecentlyModified,
    LoadingIndicator,
  },

  data: function() {
    return constants.dataDefaults();
  },

  methods: {
    route: function() {
      let path = window.location.pathname.split("/");
      let basePath = path[1];

      // Home Page
      if (basePath == "") {
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

    navigate: function(href, e) {
      if (e != undefined && e.ctrlKey == true) {
        window.open(href);
      } else {
        history.pushState(null, "", href);
        this.resetData();
        this.route();
      }
    },

    resetData: function() {
      Object.assign(this.$data, constants.dataDefaults());
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
          parent.navigate(redirectPath || "/");
        })
        .catch(function(error) {
          if (error.handled) {
            return;
          } else if (
            typeof error.response !== "undefined" &&
            [400, 422].includes(error.response.status)
          ) {
            parent.$bvToast.toast("Incorrect Username or Password ✘", {
              variant: "danger",
              noCloseButton: true,
            });
          } else {
            parent.unhandledServerErrorToast();
          }
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
      this.navigate(`/${constants.basePaths.login}`);
    },

    search: function() {
      this.navigate(
        `/${constants.basePaths.search}?${
          constants.params.searchTerm
        }=${encodeURI(this.searchTerm)}`
      );
    },

    getSearchResults: function() {
      let parent = this;
      this.searchFailed = false;
      api
        .get("/api/search", { params: { term: this.searchTerm } })
        .then(function(response) {
          parent.searchResults = [];
          response.data.forEach(function(result) {
            parent.searchResults.push(
              new SearchResult(
                result.title,
                result.lastModified,
                result.titleHighlights,
                result.contentHighlights
              )
            );
          });
        })
        .catch(function(error) {
          if (!error.handled) {
            parent.searchFailed = true;
            parent.unhandledServerErrorToast();
          }
        });
    },

    getContentForEditor: function() {
      let draftContent = localStorage.getItem(this.currentNote.title);
      if (draftContent) {
        if (confirm("Do you want to resume the saved draft?")) {
          return draftContent;
        } else {
          localStorage.removeItem(this.currentNote.title);
        }
      }
      return this.currentNote.content;
    },

    loadNote: function(title) {
      let parent = this;
      this.noteLoadFailed = false;
      api
        .get(`/api/notes/${title}`)
        .then(function(response) {
          parent.currentNote = new Note(
            response.data.title,
            response.data.lastModified,
            response.data.content
          );
          parent.updateDocumentTitle();
        })
        .catch(function(error) {
          if (error.handled) {
            return;
          } else if (
            typeof error.response !== "undefined" &&
            error.response.status == 404
          ) {
            parent.noteLoadFailedMessage = "Note not found 😞";
            parent.noteLoadFailed = true;
          } else {
            parent.unhandledServerErrorToast();
            parent.noteLoadFailed = true;
          }
        });
    },

    toggleEditMode: function() {
      let parent = this;

      // To Edit Mode
      if (this.editMode == false) {
        this.titleInput = this.currentNote.title;
        let draftContent = localStorage.getItem(this.currentNote.title);

        if (draftContent) {
          this.$bvModal
            .msgBoxConfirm(
              "There is an unsaved draft of this note stored in this browser. Do you want to resume the draft version or delete it?",
              {
                centered: true,
                title: "Resume Draft?",
                okTitle: "Resume Draft",
                cancelTitle: "Delete Draft",
                cancelVariant: "danger",
              }
            )
            .then(function(response) {
              if (response == true) {
                parent.initialContent = draftContent;
              } else {
                parent.initialContent = parent.currentNote.content;
                localStorage.removeItem(parent.currentNote.title);
              }
              parent.editMode = !parent.editMode;
            });
        } else {
          this.initialContent = this.currentNote.content;
          this.editMode = !this.editMode;
        }
      }
      // To View Mode
      else {
        this.titleInput = null;
        this.initialContent = null;
        this.editMode = !this.editMode;
      }
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
      localStorage.setItem(this.currentNote.title, this.getEditorContent());
    },

    existingTitleToast: function() {
      this.$bvToast.toast(
        "A note with this title already exists. Please try again with a new title.",
        {
          title: "Duplicate ✘",
          variant: "danger",
          noCloseButton: true,
        }
      );
    },

    saveNote: function() {
      let parent = this;
      let newContent = this.getEditorContent();

      // Title Validation
      if (typeof this.titleInput == "string") {
        this.titleInput = this.titleInput.trim();
      }
      if (!this.titleInput) {
        this.$bvToast.toast("Cannot save note without a title ✘", {
          variant: "danger",
          noCloseButton: true,
        });
        return;
      }

      // New Note
      if (this.currentNote.lastModified == null) {
        api
          .post(`/api/notes`, {
            title: this.titleInput,
            content: newContent,
          })
          .then(this.saveNoteResponseHandler)
          .catch(function(error) {
            if (error.handled) {
              return;
            } else if (
              typeof error.response !== "undefined" &&
              error.response.status == 409
            ) {
              parent.existingTitleToast();
            } else {
              parent.unhandledServerErrorToast();
            }
          });
      }

      // Modified Note
      else if (
        newContent != this.currentNote.content ||
        this.titleInput != this.currentNote.title
      ) {
        api
          .patch(`/api/notes/${this.currentNote.title}`, {
            newTitle: this.titleInput,
            newContent: newContent,
          })
          .then(this.saveNoteResponseHandler)
          .catch(function(error) {
            if (error.handled) {
              return;
            } else if (
              typeof error.response !== "undefined" &&
              error.response.status == 409
            ) {
              parent.existingTitleToast();
            } else {
              parent.unhandledServerErrorToast();
            }
          });
      }

      // No Change
      else {
        this.toggleEditMode();
        this.saveNoteToast();
      }
    },

    saveNoteResponseHandler: function(response) {
      localStorage.removeItem(this.currentNote.title);
      this.currentNote = new Note(
        response.data.title,
        response.data.lastModified,
        response.data.content
      );
      this.updateDocumentTitle();
      history.replaceState(null, "", this.currentNote.href);
      this.toggleEditMode();
      this.saveNoteToast();
    },

    saveNoteToast: function() {
      this.$bvToast.toast("Note saved ✓", {
        variant: "success",
        noCloseButton: true,
      });
    },

    cancelNote: function() {
      localStorage.removeItem(this.currentNote.title);
      if (this.currentNote.lastModified == null) {
        // Cancelling a new note
        this.currentNote = null;
        this.currentView = this.views.home;
      }
      this.toggleEditMode();
    },

    deleteNote: function() {
      let parent = this;
      this.$bvModal
        .msgBoxConfirm(
          `Are you sure you want to delete the note '${this.currentNote.title}'?`,
          {
            centered: true,
            title: "Confirm Deletion",
            okTitle: "Delete",
            okVariant: "danger",
          }
        )
        .then(function(response) {
          if (response == true) {
            api
              .delete(`/api/notes/${parent.currentNote.title}`)
              .then(function() {
                parent.navigate("/");
                parent.$bvToast.toast("Note deleted ✓", {
                  variant: "success",
                  noCloseButton: true,
                });
              })
              .catch(function(error) {
                if (!error.handled) {
                  parent.unhandledServerErrorToast();
                }
              });
          }
        });
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

    unhandledServerErrorToast: function() {
      this.$bvToast.toast(
        "Unknown error communicating with the server. Please try again.",
        {
          title: "Unknown Error",
          variant: "danger",
          noCloseButton: true,
        }
      );
    },
  },

  created: function() {
    EventBus.$on("navigate", this.navigate);
    EventBus.$on("unhandledServerError", this.unhandledServerErrorToast);
    document.addEventListener("keydown", this.keyboardShortcuts);

    let token = localStorage.getItem("token");
    if (token != null) {
      sessionStorage.setItem("token", token);
    }

    this.route();
  },

  mounted: function() {
    window.addEventListener("popstate", this.route);
  },
};
