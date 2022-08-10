<template>
  <div class="container d-flex flex-column align-items-center h-100">
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
      class="mt-3 w-100"
      :show-logo="currentView != views.home"
      @navigate-home="navigate('/')"
      @new-note="newNote()"
      @logout="logout()"
      @search="openSearch()"
    ></NavBar>

    <!-- Login -->
    <Login v-if="currentView == views.login"></Login>

    <!-- Home -->
    <div
      v-if="currentView == views.home"
      class="
        home-view
        d-flex
        flex-column
        justify-content-center
        align-items-center
        flex-grow-1
        w-100
      "
    >
      <Logo class="mb-3"></Logo>
      <SearchInput class="search-input mb-4"></SearchInput>
      <RecentlyModified class="recently-modified"></RecentlyModified>
    </div>

    <!-- Search Results -->
    <div v-if="currentView == views.search" class="w-100 pt-5">
      <!-- Searching -->
      <div v-if="searchResults == null">
        <loading-indicator
          loading-message="Searching..."
          failure-message="Search failed 😞"
          :failed="searchFailed"
        />
      </div>

      <!-- No Results -->
      <div v-else-if="searchResults.length == 0">
        <p class="text-center">No Results</p>
      </div>

      <!-- Search Results Loaded -->
      <div v-else>
        <div v-for="result in searchResults" :key="result.title" class="mb-5">
          <p class="h5 text-center clickable-link">
            <a
              v-html="result.titleHighlightsOrTitle"
              :href="result.href"
              @click.prevent="navigate(result.href, $event)"
            ></a>
          </p>
          <p
            class="text-center text-muted"
            v-html="result.contentHighlights"
          ></p>
        </div>
      </div>
    </div>

    <!-- Note -->
    <NoteViewerEditor
      v-if="currentView == this.views.note"
      class="mt-5 flex-grow-1"
      :titleToLoad="noteTitle"
      @note-deleted="noteDeletedToast"
    ></NoteViewerEditor>
  </div>
</template>

<script>
export { default } from "./App.js";
</script>
