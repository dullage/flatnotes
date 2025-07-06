import { createApp } from "vue";
import InteractiveMermaid from "./InteractiveMermaid.vue";

const WRAPPER_CLASS = "mermaid-component-wrapper";

/**
 * Cleans up any previously rendered Mermaid component wrappers from the container.
 * @param {HTMLElement} containerElement The parent element to clean up.
 */
function cleanupOldWrappers(containerElement) {
  if (!containerElement) return;

  const oldWrappers = containerElement.querySelectorAll(`.${WRAPPER_CLASS}`);
  oldWrappers.forEach((wrapperNode) => {
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
 * renders, and then renders new interactive components.
 * @param {HTMLElement} containerElement The parent element to search within.
 */
export function renderMermaidBlocks(containerElement) {
  if (!containerElement) return;

  // STEP 1: Always perform a full cleanup first.
  cleanupOldWrappers(containerElement);

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

    createApp(InteractiveMermaid, { diagramText }).mount(mountPoint);
  }
}
