<template>
  <div class="d-flex justify-content-between align-items-center">
    <!-- Logo -->
    <div>
      <img
        src="../assets/logo.svg"
        class="cursor-pointer"
        :class="{ invisible: !showLogo }"
        @click="$emit('navigate-home')"
      />
    </div>
    <div>
      <!-- New Note -->
      <button
        type="button"
        class="btn btn-sm btn-outline-primary mx-1"
        @click="$emit('new-note')"
      >
        New Note
      </button>

      <!-- Log Out -->
      <button
        type="button"
        class="btn btn-sm btn-outline-dark mx-1"
        @click="this.$emit('logout')"
      >
        Log Out
      </button>

      <!-- Search -->
      <button
        type="button"
        id="search-button"
        class="btn btn-sm btn-outline-dark mx-1"
        @click="$emit('search')"
        v-b-tooltip.hover
        title="Keyboard Shortcut: /"
      >
        <BIconSearch />
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
// Use visibility hidden instead of v-show to maintain consistent height
.invisible {
  visibility: hidden;
}

.cursor-pointer {
  cursor: pointer;
}
</style>

<script>
import { BIconSearch } from "bootstrap-vue";

export default {
  components: {
    BIconSearch,
  },

  props: {
    showLogo: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
