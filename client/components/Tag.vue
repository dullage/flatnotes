<template>
  <span class="rounded-full bg-theme-brand px-2 text-xs text-white"
    >#{{ tag }}</span
  >
</template>

<script setup>
defineProps({
  tag: String,
});
</script>
