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
      <button type="button" class="bttn" @click="$emit('new-note')">
        <b-icon icon="plus-circle"></b-icon> New Note
      </button>

      <!-- Log Out -->
      <button type="button" class="bttn" @click="$emit('logout')">
        <b-icon icon="box-arrow-right"></b-icon> Log Out
      </button>

      <!-- Search -->
      <button
        type="button"
        id="search-button"
        class="bttn"
        @click="$emit('search')"
        v-b-tooltip.hover
        title="Keyboard Shortcut: /"
      >
        <b-icon icon="search"></b-icon>
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
export default {
  props: {
    showLogo: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
