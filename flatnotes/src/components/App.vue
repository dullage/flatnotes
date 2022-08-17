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
      @navigate-home="navigate('/')"
      @new-note="newNote()"
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
      <RecentlyModified class="recently-modified"></RecentlyModified>
    </div>

    <!-- Search Results -->
    <div
      v-if="currentView == views.search"
      class="flex-grow-1 search-results-view"
    >
      <SearchInput
        :initial-value="searchTerm"
        class="search-input mb-4"
      ></SearchInput>
      <SearchResults :search-term="searchTerm" class="h-100"></SearchResults>
    </div>

    <!-- Note -->
    <NoteViewerEditor
      v-if="currentView == this.views.note"
      class="flex-grow-1"
      :titleToLoad="noteTitle"
      @note-deleted="noteDeletedToast"
    ></NoteViewerEditor>
  </div>
</template>

<script>
export { default } from "./App.js";
</script>
