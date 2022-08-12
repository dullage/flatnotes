import * as constants from "../constants";
import * as helpers from "../helpers";

import EventBus from "../eventBus";
import LoadingIndicator from "./LoadingIndicator";
import Login from "./Login";
import Logo from "./Logo";
import Mousetrap from "mousetrap";
import NavBar from "./NavBar";
import NoteViewerEditor from "./NoteViewerEditor";
import RecentlyModified from "./RecentlyModified";
import SearchInput from "./SearchInput";
import { SearchResult } from "../classes";
import api from "../api";

export default {
  name: "App",

  components: {
    RecentlyModified,
    LoadingIndicator,
    Login,
    NavBar,
    SearchInput,
    Logo,
    NoteViewerEditor,
  },

  data: function() {
    return constants.dataDefaults();
  },

  methods: {
    route: function() {
      let path = window.location.pathname.split("/");
      let basePath = path[1];

      this.$bvModal.hide("search-modal");

      // Home Page
      if (basePath == "") {
        this.updateDocumentTitle();
        this.currentView = this.views.home;
        this.$nextTick(function() {
          this.focusSearchInput();
        });
      }

      // Search
      else if (basePath == constants.basePaths.search) {
        this.updateDocumentTitle("Search");
        this.searchTerm = helpers.getSearchParam(constants.params.searchTerm);
        this.getSearchResults();
        this.currentView = this.views.search;
      }

      // New Note
      else if (basePath == constants.basePaths.new) {
        this.updateDocumentTitle("New Note");
        this.currentView = this.views.note;
      }

      // Note
      else if (basePath == constants.basePaths.note) {
        this.updateDocumentTitle();
        this.noteTitle = path[2];
        this.currentView = this.views.note;
      }

      // Login
      else if (basePath == constants.basePaths.login) {
        this.updateDocumentTitle("Log In");
        this.currentView = this.views.login;
      }
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

    updateDocumentTitle: function(suffix) {
      window.document.title = (suffix ? `${suffix} - ` : "") + "flatnotes";
    },

    logout: function() {
      sessionStorage.removeItem("token");
      localStorage.removeItem("token");
      this.navigate(`/${constants.basePaths.login}`);
    },

    getSearchResults: function() {
      let parent = this;
      this.searchFailed = false;
      api
        .get("/api/search", { params: { term: this.searchTerm } })
        .then(function(response) {
          parent.searchResults = [];
          if (response.data.length == 0) {
            parent.searchFailedIcon = "search";
            parent.searchFailedMessage = "No Results";
            parent.searchFailed = true;
          } else {
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
          }
        })
        .catch(function(error) {
          if (!error.handled) {
            parent.searchFailed = true;
            parent.unhandledServerErrorToast();
          }
        });
    },

    newNote: function() {
      this.navigate(`/${constants.basePaths.new}`);
    },

    noteDeletedToast: function() {
      this.$bvToast.toast("Note deleted ✓", {
        variant: "success",
        noCloseButton: true,
        toaster: "b-toaster-bottom-right",
      });
    },

    focusSearchInput: function() {
      document.getElementById("search-input").focus();
    },

    openSearch: function() {
      if (this.currentView == this.views.home) {
        this.focusSearchInput();
        EventBus.$emit("highlight-search-input");
      } else if (this.currentView != this.views.login) {
        this.$bvModal.show("search-modal");
      }
    },

    unhandledServerErrorToast: function() {
      this.$bvToast.toast(
        "Unknown error communicating with the server. Please try again.",
        {
          title: "Unknown Error",
          variant: "danger",
          noCloseButton: true,
          toaster: "b-toaster-bottom-right",
        }
      );
    },
  },

  created: function() {
    let parent = this;

    EventBus.$on("navigate", this.navigate);
    EventBus.$on("unhandledServerError", this.unhandledServerErrorToast);
    EventBus.$on("updateDocumentTitle", this.updateDocumentTitle);

    Mousetrap.bind("/", function() {
      parent.openSearch();
      return false;
    });

    let token = localStorage.getItem("token");
    if (token != null) {
      sessionStorage.setItem("token", token);
    }

    this.route();
  },

  mounted: function() {
    let parent = this;

    window.addEventListener("popstate", this.route);

    this.$root.$on("bv::modal::shown", function(_, modalId) {
      if (modalId == "search-modal") {
        parent.focusSearchInput();
      }
    });
  },
};
