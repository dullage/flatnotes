import { createApp } from "vue";
import InteractiveMermaid from "./InteractiveMermaid.vue";

const componentInstanceMap = new WeakMap();
const WRAPPER_CLASS = "mermaid-component-wrapper";

/**
 * Cleans up any previously rendered Mermaid Vue components within a container.
 * This function is now intended to be used primarily by renderMermaidBlocks.
 * @param {HTMLElement} containerElement The parent element to clean up.
 */
function cleanupMermaidRenders(containerElement) {
  if (!containerElement) return;

  const oldWrappers = containerElement.querySelectorAll(`.${WRAPPER_CLASS}`);
  oldWrappers.forEach((wrapperNode) => {
    if (componentInstanceMap.has(wrapperNode)) {
      componentInstanceMap.get(wrapperNode).unmount();
      componentInstanceMap.delete(wrapperNode);
    }
    wrapperNode.remove();
  });

  const processedBlocks = containerElement.querySelectorAll(
    "pre[data-mermaid-processed]",
  );
  processedBlocks.forEach((block) => {
    block.removeAttribute("data-mermaid-processed");
    block.style.display = "";
  });
}

/**
 * Finds all Mermaid code blocks in a container, cleans up any previous
 * renders, and then renders new interactive components. This is an
 * atomic "refresh" operation.
 * @param {HTMLElement} containerElement The parent element to search within.
 */
export function renderMermaidBlocks(containerElement) {
  if (!containerElement) return;

  // STEP 1: Always perform a full cleanup first.
  cleanupMermaidRenders(containerElement);

  // STEP 2: Find all potential mermaid blocks and render them.
  const mermaidNodes = containerElement.querySelectorAll("pre.lang-mermaid");

  if (mermaidNodes.length === 0) return;

  for (const node of mermaidNodes) {
    const diagramText = node.textContent;
    if (!diagramText.trim()) continue;

    node.setAttribute("data-mermaid-processed", "true");
    node.style.display = "none";

    const mountPoint = document.createElement("div");
    mountPoint.className = WRAPPER_CLASS;
    node.parentNode.insertBefore(mountPoint, node);

    const app = createApp(InteractiveMermaid, { diagramText });
    app.mount(mountPoint);

    componentInstanceMap.set(mountPoint, app);
  }
}
