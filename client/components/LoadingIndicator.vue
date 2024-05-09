<template>
  <div :class="{ 'flex items-center justify-center': loadSuccessful !== true }">
    <!-- Loading -->
    <div
      v-if="loadSuccessful === null && !props.hideLoader"
      class="loader"
    ></div>

    <!-- Failed -->
    <div
      v-else-if="loadSuccessful === false"
      class="flex flex-col items-center"
    >
      <SvgIcon
        type="mdi"
        :path="failedIconPath"
        size="4em"
        class="mb-4 text-theme-brand"
      />
      <span class="text-center text-lg text-theme-text-muted max-w-80">{{
        failedMessage
      }}</span>
    </div>

    <!-- Loaded -->
    <slot v-else-if="loadSuccessful"></slot>
  </div>
</template>

<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiTrafficCone } from "@mdi/js";
import { ref } from "vue";

const props = defineProps({ hideLoader: Boolean });

const loadSuccessful = ref(null);
const failedIconPath = ref("");
const failedMessage = ref("");

function setLoading() {
  loadSuccessful.value = null;
}

function setFailed(message, iconPath) {
  failedMessage.value = message || "Loading Failed";
  failedIconPath.value = iconPath || mdiTrafficCone;
  loadSuccessful.value = false;
}

function setLoaded() {
  loadSuccessful.value = true;
}

defineExpose({ setLoading, setFailed, setLoaded });
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
