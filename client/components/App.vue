<template>
  <div class="container d-flex flex-column h-100">
    <!-- Search Modal -->
    <b-modal id="search-modal" centered hide-footer hide-header>
      <div>
        <SearchInput></SearchInput>
      </div>
    </b-modal>

    <!-- Nav Bar -->
    <NavBar
      v-if="currentView != views.login"
      class="w-100 mb-5"
      :show-logo="currentView != views.home"
      :auth-type="authType"
      :dark-theme="darkTheme"
      @logout="logout()"
      @toggleTheme="toggleTheme()"
      @search="openSearch()"
    ></NavBar>

    <!-- Login -->
    <Login
      v-if="currentView == views.login"
      class="flex-grow-1"
      :auth-type="authType"
    ></Login>

    <!-- Home -->
    <div
      v-if="currentView == views.home"
      class="home-view align-self-center d-flex flex-column justify-content-center align-items-center flex-grow-1 w-100"
    >
      <Logo class="mb-3"></Logo>
      <SearchInput
        :initial-value="searchTerm"
        class="search-input mb-4"
      ></SearchInput>
      <div v-if="authType != null && authType != constants.authTypes.readOnly">
        <RecentlyModified
          class="recently-modified"
          :max-notes="5"
        ></RecentlyModified>
      </div>
    </div>

    <!-- Search Results -->
    <div
      v-if="currentView == views.search"
      class="flex-grow-1 search-results-view d-flex flex-column"
    >
      <SearchResults
        :search-term="searchTerm"
        class="flex-grow-1"
      ></SearchResults>
    </div>

    <!-- Note -->
    <NoteViewerEditor
      v-if="currentView == this.views.note"
      class="flex-grow-1"
      :titleToLoad="noteTitle"
      :auth-type="authType"
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
  box-shadow: 0 0 20px var(--colour-shadow);
}

.recently-modified {
  // Prevent UI from moving during load
  min-height: 190px;
}
</style>

<script>
export { default } from "./App.js";
</script>
