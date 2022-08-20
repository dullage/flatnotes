<template>
  <div class="d-flex justify-content-between align-items-center">
    <!-- Logo -->
    <Logo
      class="cursor-pointer"
      :class="{ invisible: !showLogo }"
      @click.native="$emit('navigate-home')"
      responsive
    ></Logo>

    <!-- Buttons -->
    <div>
      <!-- New Note -->
      <button type="button" class="bttn" @click="$emit('new-note')">
        <b-icon icon="plus-circle"></b-icon> New
      </button>

      <!-- Log Out -->
      <button type="button" class="bttn" @click="$emit('logout')">
        <b-icon icon="box-arrow-right"></b-icon> Log Out
      </button>

      <!-- A-Z -->
      <button type="button" class="bttn" @click="$emit('a-z')">A-Z</button>

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
import Logo from "./Logo";

export default {
  components: {
    Logo,
  },

  props: {
    showLogo: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
