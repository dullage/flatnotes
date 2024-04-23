<template>
  <button class="text-theme-text-muted">
    <span>{{ label }}</span>
  </button>
</template>

<script setup>
defineProps({
  label: String,
});
</script>
