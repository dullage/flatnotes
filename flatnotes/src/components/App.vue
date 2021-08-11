<template>
  <div class="container">
    <div>
      <!-- Header -->
      <div class="mt-4 mb-4">
        <h1 class="text-center">flatnotes</h1>
      </div>

      <!-- Buttons -->
      <div
        v-if="currentView == 2 || currentView == 3"
        class="d-flex justify-content-center mb-4"
      >
        <!-- Close -->
        <button
          v-if="currentView == 2"
          type="button"
          class="btn btn-secondary"
          @click="unloadNote"
        >
          Close
        </button>

        <!-- Edit -->
        <button
          v-if="currentView == 2"
          type="button"
          class="btn btn-warning ms-2"
          @click="editMode = true"
        >
          Edit
        </button>

        <!-- Cancel -->
        <button
          v-if="currentView == 3"
          type="button"
          class="btn btn-secondary ms-2"
          @click="editMode = false"
        >
          Cancel
        </button>

        <!-- Save -->
        <button
          v-if="currentView == 3"
          type="button"
          class="btn btn-success ms-2"
          @click="saveNote"
        >
          Save
        </button>
      </div>

      <!-- Viewer -->
      <div v-if="currentView == 2">
        <viewer :initialValue="currentNote.content" height="600px" />
      </div>

      <!-- Editor -->
      <div v-else-if="currentView == 3">
        <editor
          :initialValue="currentNote.content"
          previewStyle="tab"
          height="calc(100vh - 180px)"
          ref="toastUiEditor"
        />
      </div>

      <!-- Front Page -->
      <div v-else>
        <!-- Search Input -->
        <div class="form-group mb-4 d-flex justify-content-center">
          <input
            type="text"
            class="form-control"
            placeholder="Search"
            v-model="searchTerm"
            @change="search"
            style="max-width: 500px"
          />
        </div>

        <!-- Search Results -->
        <div v-if="currentView == 1">
          <div
            v-for="result in searchResults"
            :key="result.filename"
            class="mb-5"
          >
            <p
              class="h5 text-center clickable-link"
              v-html="result.titleHighlightsOrTitle"
              @click="loadNote(result.filename)"
            ></p>
            <p
              class="text-center text-muted"
              v-html="result.contentHighlights"
            ></p>
          </div>
        </div>

        <!-- Notes -->
        <div v-else>
          <p
            v-for="note in notesByLastModifiedDesc"
            :key="note.filename"
            class="text-center clickable-link mb-2"
            @click="loadNote(note.filename)"
          >
            {{ note.title }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export { default } from "./App.js";
</script>
