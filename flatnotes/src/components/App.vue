<template>
  <div class="container d-flex flex-column align-items-center h-100">
    <!-- Nav Bar -->
    <NavBar
      v-if="currentView != views.login"
      class="mt-2 w-100"
      :show-logo="currentView != views.home"
      @navigate-home="navigate('/')"
      @new-note="newNote()"
      @logout="logout()"
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
        class="btn btn-sm btn-outline-warning mx-1"
        @click="toggleEditMode"
      >
        Edit
      </button>

      <!-- Delete -->
      <button
        v-if="
          currentView == views.note &&
          editMode == false &&
          noteLoadFailed == false
        "
        type="button"
        class="btn btn-sm btn-outline-danger mx-1"
        @click="deleteNote"
      >
        Delete
      </button>

      <!-- Cancel -->
      <button
        v-if="currentView == views.note && editMode == true"
        type="button"
        class="btn btn-sm btn-outline-secondary mx-1"
        @click="cancelNote"
      >
        Cancel
      </button>

      <!-- Save -->
      <button
        v-if="currentView == views.note && editMode == true"
        type="button"
        class="btn btn-sm btn-outline-success mx-1"
        @click="saveNote"
      >
        Save
      </button>
    </div>

    <!-- Home -->
    <div
      v-if="currentView == views.home"
      v-on:submit.prevent="search"
      class="home-view d-flex flex-column justify-content-center align-items-center flex-grow-1 w-100"
    >
      <div class="mb-3">
        <img src="../assets/logo.svg" />
      </div>
      <form v-on:submit.prevent="search" class="w-100">
        <div class="form-group mb-4 w-100">
          <input
            type="text"
            class="form-control search-input"
            placeholder="Search"
            v-model="searchTerm"
            autofocus
          />
          <!-- TODO: Search Button -->
        </div>
      </form>
      <RecentlyModified />
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
      <!-- Search Input -->
      <form v-on:submit.prevent="search">
        <div class="form-group mb-4 d-flex justify-content-center">
          <input
            type="text"
            class="form-control"
            placeholder="Search"
            v-model="searchTerm"
            style="max-width: 500px"
            autofocus
          />
        </div>
      </form>

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
