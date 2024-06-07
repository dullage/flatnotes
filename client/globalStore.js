import * as constants from "./constants.js";

import { defineStore } from "pinia";
import { ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
  const authType = ref(constants.authTypes.password);
  const hideRecentlyModified = ref(true);

  return { authType, hideRecentlyModified };
});
