// Base Paths
export const basePaths = {
  login: "login",
  note: "note",
  search: "search",
  new: "new",
};

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

    // Note Data
    noteTitle: null,

    // Search Result Data
    searchFailed: false,
    searchTerm: null,
    searchResults: null,
  };
};
