<template>
  <div>
    <div v-if="!hideLoader && !failed" class="loader"></div>
    <div v-else-if="failed" class="flex flex-col items-center">
      <SvgIcon
        type="mdi"
        :path="failedIconPath"
        size="4em"
        class="mb-4 text-theme-brand"
      />
      <span class="text-lg text-theme-text-muted">{{ failedMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiTrafficCone } from "@mdi/js";
import { defineExpose, ref } from "vue";

defineProps({ hideLoader: Boolean });

const failed = ref(false);
const failedIconPath = ref("");
const failedMessage = ref("");

function setFailed(message, iconPath) {
  failed.value = true;
  failedMessage.value = message || "Loading Failed";
  failedIconPath.value = iconPath || mdiTrafficCone;
}

defineExpose({ setFailed });
</script>

<style scoped>
.loader,
.loader:before,
.loader:after {
  background: rgb(var(--theme-brand));
  -webkit-animation: load1 1s infinite ease-in-out;
  animation: load1 1s infinite ease-in-out;
  width: 1em;
  height: 4em;
}
.loader {
  color: rgb(var(--theme-brand));
  text-indent: -9999em;
  /* margin: 33% auto; */
  position: relative;
  font-size: 11px;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}
.loader:before,
.loader:after {
  position: absolute;
  top: 0;
  content: "";
}
.loader:before {
  left: -1.5em;
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}
.loader:after {
  left: 1.5em;
}
@-webkit-keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}
@keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}
</style>
