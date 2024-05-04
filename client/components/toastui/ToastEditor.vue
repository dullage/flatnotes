<template>
  <div ref="editorElement"></div>
</template>

<script setup>
import Editor from "@toast-ui/editor";
import codeSyntaxHighlight from "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight-all.js";
import { onMounted, ref } from "vue";

const props = defineProps({
  initialValue: String,
});

const editorElement = ref();
let toastEditor;

onMounted(() => {
  toastEditor = new Editor({
    el: editorElement.value,
    height: "100%",
    initialValue: props.initialValue,
    plugins: [codeSyntaxHighlight],
    usageStatistics: false,
  });
});

function getMarkdown() {
  return toastEditor.getMarkdown();
}

defineExpose({ getMarkdown });
</script>

<style>
@import "@toast-ui/editor/dist/toastui-editor.css";
@import "prismjs/themes/prism.css";
@import "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css";
@import "./toastui-editor-overrides.scss";
</style>
