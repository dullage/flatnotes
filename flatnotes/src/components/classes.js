class Note {
  constructor(filename, lastModified, content) {
    this.filename = filename;
    this.lastModified = lastModified;
    this.content = content;
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
