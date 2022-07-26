<template>
  <div>
    <p v-if="!failed" class="text-center">{{ loadingMessage }}</p>
    <p v-else class="text-center">{{ failureMessage }}</p>
  </div>
</template>

<script>
export default {
  props: {
    loadingMessage: { type: String, default: "Loading..." },
    failureMessage: { type: String, default: "Loading failed 😞" },
    failed: Boolean,
  },
};
</script>
