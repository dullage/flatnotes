<template>
  <div class="d-flex justify-content-between align-items-center">
    <!-- Logo -->
    <div>
      <img
        src="../assets/logo.svg"
        class="cursor-pointer"
        :class="{ invisible: !showLogo }"
        @click="navigateHome"
      />
    </div>
    <div>
      <!-- New Note -->
      <button
        type="button"
        class="btn btn-sm btn-outline-primary mx-1"
        @click="newNote"
      >
        New Note
      </button>

      <!-- Log Out -->
      <button
        type="button"
        class="btn btn-sm btn-outline-dark mx-1"
        @click="logout"
      >
        Log Out
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
export default {
  props: {
    showLogo: {
      type: Boolean,
      default: true,
    },
  },

  methods: {
    navigateHome: function () {
      this.$emit("navigate-home");
    },

    newNote: function () {
      this.$emit("new-note");
    },

    logout: function () {
      this.$emit("logout");
    },
  },
};
</script>
