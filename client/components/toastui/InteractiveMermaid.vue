<template>
  <div
    class="mermaid-wrapper"
    :class="{ 'is-fullscreen-active': isFullscreen }"
  >
    <!-- Backdrop, shown only in fullscreen -->
    <div
      v-if="isFullscreen"
      class="mermaid-fullscreen-backdrop"
      @click="toggleFullscreen"
    ></div>

    <!-- The actual interactive component -->
    <div
      ref="container"
      data-mermaid-wrapper
      class="mermaid-diagram-container"
      :class="{
        'has-error': !!errorMessage,
        'is-fullscreen': isFullscreen,
      }"
    >
      <!-- Error Box -->
      <div v-if="errorMessage" class="mermaid-error-box">
        <h4 class="mermaid-error-title">Mermaid Render Error</h4>
        <pre class="mermaid-error-text">{{ errorMessage }}</pre>
      </div>

      <!-- Content Area -->
      <div v-else class="mermaid-scroll-wrapper">
        <div
          class="mermaid-render-target"
          :class="{ 'is-dragging': isPanning }"
          :style="transformStyle"
        >
          <!-- Loading Indicator -->
          <div v-if="isRendering" class="mermaid-fullscreen-loader">
            <SvgIcon
              type="mdi"
              :path="mdiSync"
              :size="48"
              class="animate-spin"
            />
            <p>Rendering...</p>
          </div>
          <!-- Explicit Empty State -->
          <div
            v-else-if="!renderedSvg"
            class="mermaid-empty-state text-theme-text-muted"
          >
            No diagram to display
          </div>
          <!-- Unified SVG Render Target -->
          <div v-else :id="uniqueId" class="svg-wrapper" v-html="renderedSvg" />
        </div>
      </div>

      <!-- Controls (Data-Driven) -->
      <div v-if="!errorMessage && renderedSvg" class="mermaid-controls-br">
        <div class="control-grid">
          <button
            v-for="control in controls"
            :key="control.key"
            :title="control.title"
            @click="control.action"
          >
            <SvgIcon type="mdi" :path="control.icon" :size="20" />
          </button>
        </div>
      </div>
      <button
        v-if="isFullscreen"
        class="mermaid-modal-close"
        title="Close Fullscreen"
        @click="toggleFullscreen"
      >
        <SvgIcon type="mdi" :path="mdiClose" :size="24" />
      </button>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  reactive,
  computed,
  onMounted,
  onUnmounted,
  watch,
  nextTick,
} from "vue";
import mermaid from "mermaid";
import SvgIcon from "@jamescoyle/vue-icon";
import {
  mdiChevronUp,
  mdiChevronDown,
  mdiChevronLeft,
  mdiChevronRight,
  mdiContentCopy,
  mdiMagnifyPlus,
  mdiMagnifyMinus,
  mdiRestore,
  mdiCheck,
  mdiFullscreen,
  mdiFullscreenExit,
  mdiClose,
  mdiSync,
} from "@mdi/js";

const props = defineProps({ diagramText: { type: String, required: true } });

// --- Constants ---
const ZOOM_FACTOR = 1.25;
const PAN_STEP = 50;
const MAX_SCALE = 10;
const MIN_SCALE = 0.1;

// --- Reactive State & Refs ---
const container = ref(null);
const triggerElement = ref(null);
const errorMessage = ref(null);
const renderedSvg = ref("");
const isFullscreen = ref(false);
const isRendering = ref(false);
const isCopied = ref(false);
const isPanning = ref(false);
const transform = reactive({ scale: 1, x: 0, y: 0 });
const scrollPosition = reactive({ top: 0, left: 0 });

// --- Computed Properties ---
const transformStyle = computed(
  () =>
    `transform: translate(${transform.x}px, ${transform.y}px) scale(${transform.scale});`,
);
const uniqueId = `mermaid-${Math.random().toString(36).substring(2, 9)}`;

// Data-driven controls for the UI grid.
const controls = computed(() => [
  {
    key: "copy",
    title: "Copy Source",
    icon: isCopied.value ? mdiCheck : mdiContentCopy,
    action: copySource,
  },
  { key: "up", title: "Pan Up", icon: mdiChevronUp, action: () => pan("up") },
  {
    key: "zoom-in",
    title: "Zoom In",
    icon: mdiMagnifyPlus,
    action: () => zoom(ZOOM_FACTOR),
  },
  {
    key: "left",
    title: "Pan Left",
    icon: mdiChevronLeft,
    action: () => pan("left"),
  },
  { key: "reset", title: "Reset View", icon: mdiRestore, action: resetView },
  {
    key: "right",
    title: "Pan Right",
    icon: mdiChevronRight,
    action: () => pan("right"),
  },
  {
    key: "fullscreen",
    title: "Toggle Fullscreen",
    icon: isFullscreen.value ? mdiFullscreenExit : mdiFullscreen,
    action: toggleFullscreen,
  },
  {
    key: "down",
    title: "Pan Down",
    icon: mdiChevronDown,
    action: () => pan("down"),
  },
  {
    key: "zoom-out",
    title: "Zoom Out",
    icon: mdiMagnifyMinus,
    action: () => zoom(1 / ZOOM_FACTOR),
  },
]);

// --- Core Logic ---
const render = async (forceRerender = false) => {
  if (renderedSvg.value && !forceRerender) {
    return;
  }
  if (!props.diagramText.trim()) {
    renderedSvg.value = "";
    return;
  }
  isRendering.value = true;
  errorMessage.value = null;
  resetView();
  try {
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: document.body.classList.contains("dark") ? "dark" : "default",
      suppressErrorRendering: true,
    });
    const { svg } = await mermaid.render(uniqueId, props.diagramText);
    renderedSvg.value = svg;
  } catch (error) {
    console.error("Failed to render Mermaid diagram:", error);
    errorMessage.value = error.message;
  } finally {
    isRendering.value = false;
  }
};

// --- View Transformations ---
const resetView = () => Object.assign(transform, { scale: 1, x: 0, y: 0 });
const zoom = (factor) =>
  (transform.scale = Math.max(
    MIN_SCALE,
    Math.min(MAX_SCALE, transform.scale * factor),
  ));
const pan = (direction) => {
  const step = PAN_STEP / transform.scale;
  if (direction === "up") transform.y -= step;
  if (direction === "down") transform.y += step;
  if (direction === "left") transform.x -= step;
  if (direction === "right") transform.x += step;
};

// --- Event Handlers ---
const handleWheel = (e) => {
  e.preventDefault();
  zoom(e.deltaY < 0 ? ZOOM_FACTOR : 1 / ZOOM_FACTOR);
};

const handleMouseDown = (() => {
  let panStart = { x: 0, y: 0 };
  const handleMouseMove = (e) => (
    (transform.x = e.clientX - panStart.x),
    (transform.y = e.clientY - panStart.y)
  );
  const handleMouseUp = () => {
    isPanning.value = false;
    window.removeEventListener("mousemove", handleMouseMove);
    window.removeEventListener("mouseup", handleMouseUp);
  };
  return (e) => {
    const target = e.target;

    const isInteractiveContent = target.closest(
      "text, a, button, foreignObject, .mermaid-error-text",
    );

    if (isInteractiveContent) {
      return;
    }

    e.preventDefault();
    window.getSelection().removeAllRanges();
    isPanning.value = true;
    panStart = { x: e.clientX - transform.x, y: e.clientY - transform.y };
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
  };
})();

const copySource = () => {
  if (isCopied.value) return;
  navigator.clipboard.writeText(props.diagramText).then(() => {
    isCopied.value = true;
    setTimeout(() => {
      isCopied.value = false;
    }, 750);
  });
};

const toggleFullscreen = (event) => {
  if (!isFullscreen.value) {
    if (event) {
      triggerElement.value = event.currentTarget;
    }
    scrollPosition.top = window.scrollY;
    scrollPosition.left = window.scrollX;
  }
  isFullscreen.value = !isFullscreen.value;
};

// --- Watchers and Lifecycle Hooks ---
watch(isFullscreen, async (isFS) => {
  const el = container.value;
  if (!el) return;

  if (isFS) {
    // Only enable wheel zoom in fullscreen
    el.addEventListener("wheel", handleWheel);
    resetView();
  } else {
    el.removeEventListener("wheel", handleWheel);
    resetView();

    await nextTick();
    window.scrollTo(scrollPosition.left, scrollPosition.top);

    if (triggerElement.value && document.contains(triggerElement.value)) {
      setTimeout(() => {
        triggerElement.value.focus({ preventScroll: true });
      }, 0);
    }
  }
});

watch(
  () => props.diagramText,
  () => render(true),
);

onMounted(() => {
  render(true);
  const handleKeydown = (e) => {
    if (e.key === "Escape" && isFullscreen.value) {
      toggleFullscreen();
    }
  };
  window.addEventListener("keydown", handleKeydown);

  const themeObserver = new MutationObserver(() => render(true));
  themeObserver.observe(document.body, {
    attributes: true,
    attributeFilter: ["class"],
  });

  const el = container.value;
  if (el) {
    // Panning is always available, both inline and fullscreen
    el.addEventListener("mousedown", handleMouseDown);
  }

  onUnmounted(() => {
    window.removeEventListener("keydown", handleKeydown);
    themeObserver.disconnect();
    const el = container.value;
    if (el) {
      el.removeEventListener("mousedown", handleMouseDown);
      el.removeEventListener("wheel", handleWheel);
    }
  });
});
</script>
