import * as constants from "../constants";
import * as helpers from "../helpers";

import EventBus from "../eventBus";
import LoadingIndicator from "./LoadingIndicator";
import Login from "./Login";
import Logo from "./Logo";
import Mousetrap from "mousetrap";
import NavBar from "./NavBar";
import NoteList from "./NoteList";
import NoteViewerEditor from "./NoteViewerEditor";
import SearchInput from "./SearchInput";
import SearchResults from "./SearchResults";

export default {
  name: "App",

  components: {
    NoteList,
    LoadingIndicator,
    Login,
    NavBar,
    SearchInput,
    Logo,
    NoteViewerEditor,
    SearchResults,
  },

  data: function() {
    return {
      views: {
        login: 0,
        home: 1,
        note: 2,
        search: 3,
        notes: 4,
      },
      currentView: 1,

      noteTitle: null,
      searchTerm: null,
    };
  },

  methods: {
    route: function() {
      let path = window.location.pathname.split("/");
      let basePath = `/${path[1]}`;

      this.$bvModal.hide("search-modal");

      // Home Page
      if (basePath == constants.basePaths.home) {
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
        this.noteTitle = decodeURIComponent(path[2]);
        this.currentView = this.views.note;
      }

      // Notes
      else if (basePath == constants.basePaths.notes) {
        this.updateDocumentTitle();
        this.currentView = this.views.notes;
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
        this.noteTitle = null;
        this.searchTerm = null;
        this.route();
      }
    },

    updateDocumentTitle: function(suffix) {
      window.document.title = (suffix ? `${suffix} - ` : "") + "flatnotes";
    },

    logout: function() {
      sessionStorage.removeItem("token");
      localStorage.removeItem("token");
      this.navigate(constants.basePaths.login);
    },

    newNote: function() {
      this.navigate(constants.basePaths.new);
    },

    az: function() {
      let params = new URLSearchParams();
      params.set(constants.params.searchTerm, "*");
      params.set(constants.params.sortBy, constants.searchSortOptions.title);
      params.set(constants.params.showHighlights, false);
      this.navigate(`${constants.basePaths.search}?${params.toString()}`);
    },

    noteDeletedToast: function() {
      this.$bvToast.toast("Note deleted ✓", {
        variant: "success",
        noCloseButton: true,
        toaster: "b-toaster-bottom-right",
      });
    },

    focusSearchInput: function() {
      let input = document.getElementById("search-input");
      input.focus();
      input.select();
    },

    openSearch: function() {
      if ([this.views.home, this.views.search].includes(this.currentView)) {
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

    this.constants = constants;

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
