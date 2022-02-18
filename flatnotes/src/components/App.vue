<template>
  <div class="container">
    <div>
      <!-- Header -->
      <div class="mt-4 mb-4">
        <h1 class="h1 clickable-link text-center"><a href="/">flatnotes</a></h1>
      </div>

      <!-- Login -->
      <div
        v-if="currentView == views.login"
        class="d-flex justify-content-center"
      >
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

      <!-- Buttons -->
      <div v-if="currentView != 4" class="d-flex justify-content-center mb-4">
        <!-- Logout -->
        <button
          v-if="currentView == views.home"
          type="button"
          class="btn btn-light mx-1"
          @click="logout"
        >
          Logout
        </button>

        <!-- New -->
        <button
          v-if="currentView == views.home"
          type="button"
          class="btn btn-primary mx-1"
          @click="newNote"
        >
          New
        </button>

        <!-- Close -->
        <a href="/">
          <button
            v-if="currentView == 2 && editMode == false"
            type="button"
            class="btn btn-secondary mx-1"
          >
            Close
          </button>
        </a>

        <!-- Edit -->
        <button
          v-if="currentView == views.note && editMode == false"
          type="button"
          class="btn btn-warning mx-1"
          @click="toggleEditMode"
        >
          Edit
        </button>

        <!-- Delete -->
        <button
          v-if="currentView == views.note && editMode == false"
          type="button"
          class="btn btn-danger mx-1"
          @click="deleteNote"
        >
          Delete
        </button>

        <!-- Cancel -->
        <button
          v-if="currentView == views.note && editMode == true"
          type="button"
          class="btn btn-secondary mx-1"
          @click="cancelNote"
        >
          Cancel
        </button>

        <!-- Save -->
        <button
          v-if="currentView == views.note && editMode == true"
          type="button"
          class="btn btn-success mx-1"
          @click="saveNote"
        >
          Save
        </button>
      </div>

      <!-- Search Input -->
      <form
        v-if="[views.search, views.home].includes(currentView)"
        v-on:submit.prevent="search"
      >
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

      <!-- Note -->
      <div v-if="currentView == views.note && currentNote != null">
        <!-- Viewer -->
        <div v-if="editMode == false">
          <viewer :initialValue="currentNote.content" height="600px" />
        </div>

        <!-- Editor -->
        <div v-else>
          <input type="text" class="form-control" v-model="titleInput" />
          <editor
            :initialValue="getContentForEditor()"
            previewStyle="tab"
            height="calc(100vh - 180px)"
            ref="toastUiEditor"
            @change="startDraftSaveTimeout"
          />
        </div>
      </div>

      <!-- Search -->
      <div v-if="currentView == views.search">
        <!-- Search Results -->
        <div v-if="searchResults">
          <div
            v-for="result in searchResults"
            :key="result.filename"
            class="mb-5"
          >
            <p class="h5 text-center clickable-link">
              <a v-html="result.titleHighlightsOrTitle" :href="result.href"></a>
            </p>
            <p
              class="text-center text-muted"
              v-html="result.contentHighlights"
            ></p>
          </div>
        </div>
      </div>

      <!-- Home -->
      <div v-if="currentView == views.home">
        <p
          v-for="note in notesByLastModifiedDesc"
          class="text-center clickable-link mb-2"
          :key="note.filename"
        >
          <a :href="note.href">{{ note.title }}</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export { default } from "./App.js";
</script>
