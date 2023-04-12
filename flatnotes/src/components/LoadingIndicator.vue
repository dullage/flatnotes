<template>
  <div class="d-flex justify-content-center">
    <div v-if="showLoader && !failed" class="loader"></div>
    <div
      v-else-if="failed"
      class="d-flex flex-column align-items-center failure-message"
    >
      <b-icon
        class="failed-icon mb-3"
        :icon="failedBootstrapIcon || 'cone-striped'"
      ></b-icon>
      <p>{{ failedMessage }}</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "../colours";

p {
  color: var(--colour-text-muted);
}

.failed-icon {
  color: var(--colour-brand);
  font-size: 60px;
}

.failure-message {
  max-width: 300px;
  text-align: center;
}

.loader,
.loader:before,
.loader:after {
  background: var(--colour-brand);
  -webkit-animation: load1 1s infinite ease-in-out;
  animation: load1 1s infinite ease-in-out;
  width: 1em;
  height: 4em;
}
.loader {
  color: var(--colour-brand);
  text-indent: -9999em;
  margin: 33% auto;
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

<script>
export default {
  props: {
    showLoader: { type: Boolean, default: true },
    failed: { type: Boolean },
    failedBootstrapIcon: { type: String },
    failedMessage: { type: String, default: "Loading Failed" },
  },
};
</script>
