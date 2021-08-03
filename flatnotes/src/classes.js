class Note {
  constructor(filename, lastModified) {
    this.filename = filename;
    this.lastModified = lastModified;
  }

  get title() {
    return this.filename.slice(0, -3);
  }
}

class SearchResult extends Note {
  constructor(filename, lastModified, titleHighlights, contentHighlights) {
    super(filename, lastModified);
    this.titleHighlights = titleHighlights;
    this.contentHighlights = contentHighlights;
  }

  get titleHighlightsOrTitle() {
    return this.titleHighlights ? this.titleHighlights : this.title;
  }
}

export { Note, SearchResult };
