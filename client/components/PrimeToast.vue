<template>
  <Toast position="bottom-right" :pt="style" />
</template>

<script setup>
import Toast from "primevue/toast";

const style = {
  message: "flex flex-col items-end ml-[20px]",
  container: ({ props }) => ({
    class: [
      "mt-2 px-3 py-2 rounded-lg max-w-96",
      "bg-theme-background dark:bg-theme-background-elevated border border-l-2 border-theme-border shadow-md",
      {
        "border-l-theme-success": props.message.severity == "success",
        "border-l-theme-danger": props.message.severity == "error",
      },
    ],
  }),
  icon: "invisible h-0 w-0",
  summary: "font-bold",
};
</script>
