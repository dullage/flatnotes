<template>
  <div class="container d-flex flex-column h-100">
    <!-- Search Modal -->
    <b-modal id="search-modal" centered hide-footer hide-header>
      <div class="d-flex flex-column align-items-center">
        <Logo class="mb-4"></Logo>
        <SearchInput></SearchInput>
      </div>
    </b-modal>

    <!-- Nav Bar -->
    <NavBar
      v-if="currentView != views.login"
      class="w-100 mb-5"
      :show-logo="currentView != views.home"
      @navigate-home="navigate(constants.basePaths.home)"
      @new-note="newNote()"
      @a-z="navigate(constants.basePaths.notes)"
      @logout="logout()"
      @search="openSearch()"
    ></NavBar>

    <!-- Login -->
    <Login v-if="currentView == views.login" class="flex-grow-1"></Login>

    <!-- Home -->
    <div
      v-if="currentView == views.home"
      class="
        home-view
        align-self-center
        d-flex
        flex-column
        justify-content-center
        align-items-center
        flex-grow-1
        w-100
      "
    >
      <Logo class="mb-3"></Logo>
      <SearchInput
        :initial-value="searchTerm"
        class="search-input mb-4"
      ></SearchInput>
      <NoteList
        class="recently-modified"
        mini-header="Recently Modified"
        :num-recently-modified="5"
        :show-loader="false"
        centered
      ></NoteList>
    </div>

    <!-- Search Results -->
    <div
      v-if="currentView == views.search"
      class="flex-grow-1 search-results-view d-flex flex-column"
    >
      <SearchInput
        :initial-value="searchTerm"
        class="search-input mb-4"
      ></SearchInput>
      <SearchResults
        :search-term="searchTerm"
        class="flex-grow-1"
      ></SearchResults>
    </div>

    <!-- Notes -->
    <NoteList
      v-if="currentView == views.notes"
      class="flex-grow-1"
      grouped
      show-last-modified
    ></NoteList>

    <!-- Note -->
    <NoteViewerEditor
      v-if="currentView == this.views.note"
      class="flex-grow-1"
      :titleToLoad="noteTitle"
      @note-deleted="noteDeletedToast"
    ></NoteViewerEditor>
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

.home-view {
  max-width: 500px;
}

.search-results-view {
  max-width: 700px;
}

.search-input {
  box-shadow: 0 0 20px $drop-shadow;
}

.recently-modified {
  // Prevent UI from moving during load
  min-height: 180px;
}
</style>

<script>
export { default } from "./App.js";
</script>
