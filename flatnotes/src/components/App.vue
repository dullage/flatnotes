<template>
  <div class="container">
    <div>
      <!-- Header -->
      <div class="mt-4 mb-4">
        <h1 class="text-center">flatnotes</h1>
      </div>

      <!-- Buttons -->
      <div v-if="currentView != 4" class="d-flex justify-content-center mb-4">
        <!-- Logout -->
        <button
          v-if="currentView == 0"
          type="button"
          class="btn btn-light mx-1"
          @click="logout"
        >
          Logout
        </button>

        <!-- New -->
        <button
          v-if="currentView == 0"
          type="button"
          class="btn btn-primary mx-1"
          @click="newNote"
        >
          New
        </button>

        <!-- Close -->
        <button
          v-if="currentView == 2"
          type="button"
          class="btn btn-secondary mx-1"
          @click="unloadNote"
        >
          Close
        </button>

        <!-- Edit -->
        <button
          v-if="currentView == 2"
          type="button"
          class="btn btn-warning mx-1"
          @click="editMode = true"
        >
          Edit
        </button>

        <!-- Cancel -->
        <button
          v-if="currentView == 3"
          type="button"
          class="btn btn-secondary mx-1"
          @click="editMode = false"
        >
          Cancel
        </button>

        <!-- Save -->
        <button
          v-if="currentView == 3"
          type="button"
          class="btn btn-success mx-1"
          @click="saveNote"
        >
          Save
        </button>
      </div>

      <!-- Login -->
      <div v-if="currentView == 4" class="d-flex justify-content-center">
        <form v-on:submit.prevent="login">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              id="username"
              autocomplete="username"
              v-model="usernameInput"
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              autocomplete="current-password"
              v-model="passwordInput"
            />
          </div>
          <div class="mb-3 form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="rememberMe"
              v-model="rememberMeInput"
            />
            <label class="form-check-label" for="rememberMe">Remember Me</label>
          </div>
          <button type="submit" class="btn btn-primary">Log In</button>
        </form>
      </div>

      <!-- Viewer -->
      <div v-else-if="currentView == 2">
        <viewer :initialValue="currentNote.content" height="600px" />
      </div>

      <!-- Editor -->
      <div v-else-if="currentView == 3">
        <input type="text" class="form-control" v-model="newFilename" />
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
        <form v-on:submit.prevent="search">
          <div class="form-group mb-4 d-flex justify-content-center">
            <input
              type="text"
              class="form-control"
              placeholder="Search"
              v-model="searchTerm"
              style="max-width: 500px"
            />
          </div>
        </form>

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
