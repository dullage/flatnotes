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
      <!-- New Note -->
      <a
        v-if="showNewButton"
        :href="constants.basePaths.new"
        class="bttn"
        @click.prevent="navigate(constants.basePaths.new, $event)"
      >
        <b-icon icon="plus-circle"></b-icon><span>New Note</span>
      </a>

      <!-- Menu -->
      <b-dropdown
        menu-class="menu"
        toggle-class="bttn text-decoration-none"
        size="md"
        variant="link"
        no-caret
        right
      >
        <template #button-content>
          <b-icon icon="list"></b-icon><span>Menu</span>
        </template>

        <!-- Search -->
        <!-- Note: We use .capture.native.stop here to prevent button from gaining focus after the menu is closed. -->
        <b-dropdown-item-button
          button-class="bttn d-flex align-items-center"
          @click.capture.native.stop="$emit('search')"
        >
          <b-icon icon="search" font-scale="0.8" class="mr-2"></b-icon>
          <span class="mr-3">Search</span>
          <span class="keyboard-shortcut" title="Keyboard Shortcut">/</span>
        </b-dropdown-item-button>

        <!-- All Notes -->
        <b-dropdown-item
          link-class="bttn d-flex align-items-center"
          :href="azHref"
          @click.prevent="navigate(azHref, $event)"
        >
          <b-icon icon="files" font-scale="0.8" class="mr-2"></b-icon>
          <span>All Notes</span>
        </b-dropdown-item>

        <!-- Toggle Theme -->
        <b-dropdown-item-button
          button-class="bttn d-flex align-items-center"
          @click="$emit('toggleTheme')"
        >
          <b-icon
            :icon="darkTheme ? 'sun' : 'moon'"
            font-scale="0.8"
            class="mr-2"
          >
          </b-icon>
          <span>Toggle Theme</span>
        </b-dropdown-item-button>

        <!-- Log Out -->
        <b-dropdown-divider v-if="showLogOutButton"></b-dropdown-divider>
        <b-dropdown-item-button
          v-if="showLogOutButton"
          button-class="bttn d-flex align-items-center"
          @click="$emit('logout')"
        >
          <b-icon icon="box-arrow-right" font-scale="0.8" class="mr-2"></b-icon>
          <span>Log Out</span>
        </b-dropdown-item-button>
      </b-dropdown>
    </div>
  </div>
</template>

<style lang="scss">
// Use visibility hidden instead of v-show to maintain consistent height
.invisible {
  visibility: hidden;
}

.menu {
  background-color: var(--colour-background);
  color: var(--colour-text);
  border: 1px solid var(--colour-border);

  hr {
    border-top: 1px solid var(--colour-border);
  }
}

.keyboard-shortcut {
  background-color: var(--colour-background-elevated);
  padding: 0.1em 0.75em;
  border: 1px solid var(--colour-border);
  border-radius: 4px;
  font-size: 0.75em;
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
    authType: { type: String, default: null },
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

    showLogOutButton: function () {
      return (
        this.authType != null &&
        ![constants.authTypes.none, constants.authTypes.readOnly].includes(
          this.authType
        )
      );
    },

    showNewButton: function () {
      return (
        this.authType != null && this.authType != constants.authTypes.readOnly
      );
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
