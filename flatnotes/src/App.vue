<template>
  <div class="container">
    <div class="row">
      <div class="col"></div>
      <div class="col-6">
        <!-- Header -->
        <div class="mt-4 mb-4">
          <h1 class="text-center">flatnotes</h1>
        </div>

        <!-- Search Input -->
        <div class="form-group mb-4">
          <input
            type="text"
            class="form-control"
            placeholder="Search"
            v-model="searchTerm"
            @change="search"
          />
        </div>

        <!-- Search Results -->
        <div v-if="searchTerm">
          <div
            v-for="result in searchResults"
            :key="result.filename"
            class="mb-5"
          >
            <p
              class="h5 text-center"
              v-html="result.titleHighlightsOrTitle"
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
            class="text-center"
          >
            {{ note.title }}
          </p>
        </div>
      </div>
      <div class="col"></div>
    </div>
  </div>
</template>

<script>
export { default } from "./App.js";
</script>
