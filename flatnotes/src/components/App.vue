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
      class="mt-2 w-100"
      :show-logo="currentView != views.home"
      @navigate-home="navigate('/')"
      @new-note="newNote()"
      @logout="logout()"
      @search="openSearch()"
    ></NavBar>

    <!-- Login -->
    <Login v-if="currentView == views.login"></Login>

    <!-- Buttons -->
    <div class="d-flex justify-content-center mb-4">
      <!-- Edit -->
      <button
        v-if="
          currentView == views.note &&
          editMode == false &&
          noteLoadFailed == false
        "
        type="button"
        class="bttn"
        @click="toggleEditMode"
        v-b-tooltip.hover
        title="Keyboard Shortcut: e"
      >
        <b-icon icon="pencil-square"></b-icon> Edit
      </button>

      <!-- Delete -->
      <button
        v-if="
          currentView == views.note &&
          editMode == false &&
          noteLoadFailed == false
        "
        type="button"
        class="bttn"
        @click="deleteNote"
      >
        <b-icon icon="trash"></b-icon> Delete
      </button>

      <!-- Cancel -->
      <button
        v-if="currentView == views.note && editMode == true"
        type="button"
        class="bttn"
        @click="cancelNote"
      >
        <b-icon icon="arrow-return-left"></b-icon> Cancel
      </button>

      <!-- Save -->
      <button
        v-if="currentView == views.note && editMode == true"
        type="button"
        class="bttn"
        @click="saveNote"
      >
        <b-icon icon="check-square"></b-icon> Save
      </button>
    </div>

    <!-- Home -->
    <div
      v-if="currentView == views.home"
      v-on:submit.prevent="search"
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

    <!-- Note -->
    <div v-if="currentView == views.note" class="w-100">
      <!-- Loading -->
      <div v-if="currentNote == null">
        <loading-indicator
          :failure-message="noteLoadFailedMessage"
          :failed="noteLoadFailed"
        />
      </div>

      <!-- Note Loaded -->
      <div v-else>
        <h2 v-if="editMode == false" class="mb-4">{{ currentNote.title }}</h2>
        <input
          v-else
          type="text"
          class="h2 title-input"
          v-model="titleInput"
          placeholder="Title"
        />

        <!-- Viewer -->
        <div class="mb-4 note">
          <div v-if="editMode == false" class="note-viewer">
            <viewer
              :initialValue="currentNote.content"
              height="600px"
              :options="viewerOptions"
            />
          </div>

          <!-- Editor -->
          <div v-else>
            <editor
              :initialValue="initialContent"
              initialEditType="markdown"
              previewStyle="tab"
              height="calc(100vh - 230px)"
              ref="toastUiEditor"
              :options="editorOptions"
              @change="startDraftSaveTimeout"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Search -->
    <div v-if="currentView == views.search" class="w-100">
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
  </div>
</template>

<script>
export { default } from "./App.js";
</script>
