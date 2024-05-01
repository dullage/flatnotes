<template>
  <Menu ref="menu" :pt="style">
    <template #item="{ item, props }">
      <IconLabel
        :iconPath="item.icon"
        :label="item.label"
        v-bind="props.action"
      />
    </template>
  </Menu>
</template>
<script setup>
import Menu from "primevue/menu";
import { ref } from "vue";

import IconLabel from "./IconLabel.vue";

const menu = ref();

const style = {
  root: "border p-1 rounded border-theme-border",
  menuitem: ({ context }) => ({
    class: [
      "text-theme-text-muted rounded px-2 py-1",
      "hover:bg-theme-background-tint hover:dark:bg-theme-background-elevated hover:cursor-pointer",
      {
        "bg-theme-background-tint dark:bg-theme-background-elevated":
          context.focused,
      },
    ],
  }),
  separator: "border-t border-theme-border my-2",
};

function toggle(event) {
  menu.value.toggle(event);
}

defineExpose({ toggle });
</script>
