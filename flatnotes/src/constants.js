import codeSyntaxHighlight from "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight-all.js";

export const markdownExt = "md";

// Base Paths
export const basePaths = { login: "login", note: "note", search: "search" };

// Params
export const params = { searchTerm: "term", redirect: "redirect" };

// Initial State
export const dataDefaults = function() {
  return {
    // Views
    views: {
      login: 0,
      home: 1,
      note: 2,
      search: 3,
    },

    // State
    currentView: 1,
    editMode: false,
    draftSaveTimeout: null,

    // Login Data
    usernameInput: null,
    passwordInput: null,
    rememberMeInput: false,

    // Search Data
    searchFailed: false,

    // Note Data
    searchTerm: null,
    searchResults: null,
    currentNote: null,
    titleInput: null,
    initialContent: null,
    noteLoadFailed: false,
    noteLoadFailedMessage: "Loading failed 😞",

    // Toast UI Plugins
    viewerOptions: { plugins: [codeSyntaxHighlight] },
    editorOptions: { plugins: [codeSyntaxHighlight] },
  };
};
