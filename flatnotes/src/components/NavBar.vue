<template>
  <div class="d-flex justify-content-between align-items-center">
    <!-- Logo -->
    <a
      :href="constants.basePaths.home"
      @click.prevent="navigate(constants.basePaths.home, $event)"
    >
      <Logo :class="{ invisible: !showLogo }" responsive></Logo>
    </a>

    <!-- Buttons -->
    <div class="d-flex">
      <!-- Log Out -->
      <button
        v-if="showLogOut"
        type="button"
        class="bttn"
        @click="$emit('logout')"
      >
        <b-icon icon="box-arrow-right"></b-icon> Log Out
      </button>

      <!-- New Note -->
      <a
        :href="constants.basePaths.new"
        class="bttn"
        @click.prevent="navigate(constants.basePaths.new, $event)"
        v-b-tooltip.hover
        title="Create a New Note"
      >
        <b-icon icon="plus-circle"></b-icon> New
      </a>

      <!-- Theme Toggle -->
      <button
        type="button"
        id="theme-button"
        class="bttn"
        @click="$emit('toggleTheme')"
        v-b-tooltip.hover
        title="Toggle Theme"
      >
        <b-icon :icon="darkTheme ? 'sun' : 'moon'"></b-icon>
      </button>

      <!-- A-Z -->
      <a
        :href="azHref"
        class="bttn"
        @click.prevent="navigate(azHref, $event)"
        v-b-tooltip.hover
        title="Show All Notes"
        >A-Z</a
      >

      <!-- Search -->
      <button
        type="button"
        id="search-button"
        class="bttn"
        @click="$emit('search')"
        v-b-tooltip.hover
        title="Search (Keyboard Shortcut: /)"
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
</style>

<script>
import * as constants from "../constants";

import EventBus from "../eventBus";
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
    showLogOut: { type: Boolean, default: false },
    darkTheme: { type: Boolean, default: false },
  },

  computed: {
    azHref: function () {
      let params = new URLSearchParams();
      params.set(constants.params.searchTerm, "*");
      params.set(constants.params.sortBy, constants.searchSortOptions.title);
      params.set(constants.params.showHighlights, false);
      return `${constants.basePaths.search}?${params.toString()}`;
    },
  },

  methods: {
    navigate: function (href, event) {
      EventBus.$emit("navigate", href, event);
    },
  },

  created: function () {
    this.constants = constants;
  },
};
</script>
