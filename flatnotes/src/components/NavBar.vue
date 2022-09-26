<template>
  <div class="d-flex justify-content-between align-items-center">
    <!-- Logo -->
    <a
      :href="constants.basePaths.home"
      @click.prevent="navigate(constants.basePaths.home, $event)"
    >
      <Logo
        :class="{ invisible: !showLogo }"
        responsive
      ></Logo>
    </a>

    <!-- Buttons -->
    <div class="d-flex">
      <!-- New Note -->
      <a
        :href="constants.basePaths.new"
        class="bttn"
        @click.prevent="navigate(constants.basePaths.new, $event)"
      >
        <b-icon icon="plus-circle"></b-icon> New
      </a>

      <!-- Log Out -->
      <button type="button" class="bttn" @click="$emit('logout')">
        <b-icon icon="box-arrow-right"></b-icon> Log Out
      </button>

      <!-- A-Z -->
      <a :href="azHref" class="bttn" @click.prevent="navigate(azHref, $event)"
        >A-Z</a
      >

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
