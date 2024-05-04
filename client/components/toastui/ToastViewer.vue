<template>
  <div ref="viewerElement"></div>
</template>

<script setup>
import codeSyntaxHighlight from "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight-all.js";
import Viewer from "@toast-ui/editor/dist/toastui-editor-viewer";
import { onMounted, ref } from "vue";

const props = defineProps({
  initialValue: String,
});

const viewerElement = ref();

onMounted(() => {
  new Viewer({
    el: viewerElement.value,
    initialValue: props.initialValue,
    plugins: [codeSyntaxHighlight],
    usageStatistics: false,
  });
});
</script>

<style>
@import "@toast-ui/editor/dist/toastui-editor-viewer.css";
@import "prismjs/themes/prism.css";
@import "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css";
@import "./toastui-editor-overrides.scss";
</style>
