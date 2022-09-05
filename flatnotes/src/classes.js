import * as constants from "./constants";

class Note {
  constructor(title, lastModified, content) {
    this.title = title;
    this.lastModified = lastModified;
    this.content = content;
  }

  get href() {
    return `${constants.basePaths.note}/${encodeURIComponent(this.title)}`;
  }

  get lastModifiedAsDate() {
    return new Date(this.lastModified * 1000);
  }

  get lastModifiedAsString() {
    return this.lastModifiedAsDate.toLocaleString();
  }
}

class SearchResult extends Note {
  constructor(searchResult) {
    super(searchResult.title, searchResult.lastModified);
    this.rank = searchResult.rank;
    this.titleHighlights = searchResult.titleHighlights;
    this.contentHighlights = searchResult.contentHighlights;
    this.tagMatches = searchResult.tagMatches;
  }

  get titleHighlightsOrTitle() {
    return this.titleHighlights ? this.titleHighlights : this.title;
  }
}

export { Note, SearchResult };
