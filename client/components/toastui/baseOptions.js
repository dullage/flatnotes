import codeSyntaxHighlight from "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight-all.js";
import router from "../../router.js";
import katex from "katex";

/*
 * Sourced from toast-ui. Their autolink options are
 * either override their built in functionality or
 * use their built in functionality. We'd like to have
 * both so this is the source of their parsers.
 */
const DOMAIN = "(?:[w-]+.)*[A-Za-z0-9-]+.[A-Za-z0-9-]+";
const PATH = "[^<\\s]*[^<?!.,:*_?~\\s]";
const EMAIL = "[\\w.+-]+@(?:[\\w-]+\\.)+[\\w-]+";
function trimUnmatchedTrailingParens(source) {
  const trailingParen = /\)+$/.exec(source);
  if (trailingParen) {
    let count = 0;
    for (const ch of source) {
      if (ch === "(") {
        if (count < 0) {
          count = 1;
        } else {
          count += 1;
        }
      } else if (ch === ")") {
        count -= 1;
      }
    }

    if (count < 0) {
      const trimCount = Math.min(-count, trailingParen[0].length);
      return source.substring(0, source.length - trimCount);
    }
  }
  return source;
}

function trimTrailingEntity(source) {
  return source.replace(/&[A-Za-z0-9]+;$/, "");
}
export function parseEmailLink(source) {
  const reEmailLink = new RegExp(EMAIL, "g");
  const result = [];
  let m;
  while ((m = reEmailLink.exec(source))) {
    const text = m[0];
    if (!/[_-]+$/.test(text)) {
      result.push({
        text,
        range: [m.index, m.index + text.length - 1],
        url: `mailto:${text}`,
      });
    }
  }

  return result;
}

export function parseUrlLink(source) {
  const reWwwAutolink = new RegExp(`(www|https?://)\.${DOMAIN}${PATH}`, "g");
  const result = [];
  let m;

  while ((m = reWwwAutolink.exec(source))) {
    const text = trimTrailingEntity(trimUnmatchedTrailingParens(m[0]));
    const scheme = m[1] === "www" ? "http://" : "";
    result.push({
      text,
      range: [m.index, m.index + text.length - 1],
      url: `${scheme}${text}`,
    });
  }

  return result;
}
// end of raw toast-ui source

function parseWikiLink(source) {
  const matched = source.matchAll(/\[\[(.*)\]\]/g);
  if (matched) {
    return Array.from(matched).map((match) => {
      const text = match[1];
      return {
        text,
        url: `${router.resolve({ name: "note", params: { title: text.trim() } }).href}`,
        range: [match.index, match.index + match[0].length - 1],
      };
    });
  }

  return null;
}

function extendedAutolinks(source) {
  return [
    ...parseUrlLink(source),
    ...parseEmailLink(source),
    ...parseWikiLink(source),
  ].sort((a, b) => a.range[0] - b.range[0]);
}

const customHTMLRenderer = {
  // Add id attribute to headings
  heading(node, { entering, getChildrenText, origin }) {
    const original = origin();
    if (entering) {
      original.attributes = {
        id: getChildrenText(node)
          .toLowerCase()
          .replace(/[^a-z0-9-\s]*/g, "")
          .trim()
          .replace(/\s/g, "-"),
      };
    }
    return original;
  },
  // Convert relative hash links to absolute links
  link(_, { entering, origin }) {
    const original = origin();
    if (entering) {
      const href = original.attributes.href;
      if (href.startsWith("#")) {
        const targetRoute = {
          ...router.currentRoute.value,
          hash: href,
        };
        original.attributes.href = router.resolve(targetRoute).href;
      }
    }
    return original;
  },
};

function latexPlugin() {
  const toHTMLRenderers = {
    latex(node) {
      const html = katex.renderToString(node.literal, {
        throwOnError: false
      });

      return [
        { type: 'openTag', tagName: 'div', outerNewLine: true },
        { type: 'html', content: html },
        { type: 'closeTag', tagName: 'div', outerNewLine: true }
      ]
    }
  }

    return { toHTMLRenderers }
}

const baseOptions = {
  height: "100%",
  plugins: [codeSyntaxHighlight, latexPlugin],
  customHTMLRenderer: customHTMLRenderer,
  usageStatistics: false,
  extendedAutolinks,
};

export default baseOptions;
