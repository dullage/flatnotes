import * as constants from "./constants";

class Note {
  constructor(title, lastModified, content) {
    this.title = title;
    this.lastModified = lastModified;
    this.content = content;
  }

  get href() {
    return `/${constants.basePaths.note}/${this.title}`;
  }
}

class SearchResult extends Note {
  constructor(title, lastModified, titleHighlights, contentHighlights) {
    super(title, lastModified);
    this.titleHighlights = titleHighlights;
    this.contentHighlights = contentHighlights;
  }

  get titleHighlightsOrTitle() {
    return this.titleHighlights ? this.titleHighlights : this.title;
  }
}

export { Note, SearchResult };
