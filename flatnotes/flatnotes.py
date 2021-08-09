import glob
import logging
import os
from datetime import datetime
from typing import List, Tuple
from fastapi.params import File

import whoosh
from whoosh import writing
from whoosh.fields import ID, STORED, TEXT, SchemaClass
from whoosh.index import Index
from whoosh.qparser import MultifieldParser
from whoosh.searching import Hit


class FilenameContainsPathError(Exception):
    def __init__(self, message="Specified filename contains path information"):
        self.message = message
        super().__init__(self.message)


class IndexSchema(SchemaClass):
    filename = ID(unique=True, stored=True)
    last_modified = STORED()
    title = TEXT(field_boost=2)
    content = TEXT()


class Note:
    def __init__(
        self, flatnotes: "Flatnotes", filename: str, new: bool = False
    ) -> None:
        if not self._is_path_safe(filename):
            raise FilenameContainsPathError
        self._flatnotes = flatnotes
        self._filename = filename
        if new and os.path.exists(self.filepath):
            raise FileExistsError
        elif new:
            open(self.filepath, "w").close()

    @property
    def filepath(self):
        return os.path.join(self._flatnotes.dir, self._filename)

    @property
    def title(self):
        return os.path.splitext(self._filename)[0]

    @property
    def last_modified(self):
        return os.path.getmtime(self.filepath)

    # Editable Properties
    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        if not self._is_path_safe(new_filename):
            raise FilenameContainsPathError
        new_filepath = os.path.join(self._flatnotes.dir, new_filename)
        os.rename(self.filepath, new_filepath)
        self._filename = new_filename

    @property
    def content(self):
        with open(self.filepath, "r") as f:
            return f.read()

    @content.setter
    def content(self, new_content):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError
        with open(self.filepath, "w") as f:
            f.write(new_content)

    def delete(self):
        os.remove(self.filepath)

    # Functions
    def _is_path_safe(self, filename: str) -> bool:
        """Return False if the declared filename contains path
        information e.g. '../note.md' or 'folder/note.md'."""
        return os.path.split(filename)[0] == ""


class NoteHit(Note):
    def __init__(self, flatnotes: "Flatnotes", hit: Hit) -> None:
        super().__init__(flatnotes, hit["filename"])
        self.title_highlights = hit.highlights("title", text=self.title)
        self.content_highlights = hit.highlights(
            "content",
            text=self.content,
        )


class Flatnotes(object):
    def __init__(self, dir: str) -> None:
        if not os.path.exists(dir):
            raise NotADirectoryError(f"'{dir}' is not a valid directory.")
        self.dir = dir

        self.index = self._load_index()
        self.last_index_update = None
        self.update_index()

    @property
    def index_dir(self):
        return os.path.join(self.dir, ".flatnotes")

    def _load_index(self) -> Index:
        """Load the note index or create new if not exists."""
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
        if whoosh.index.exists_in(self.index_dir):
            logging.info("Existing index loaded")
            return whoosh.index.open_dir(self.index_dir)
        else:
            logging.info("New index created")
            return whoosh.index.create_in(self.index_dir, IndexSchema)

    def _add_note_to_index(
        self, writer: writing.IndexWriter, note: Note
    ) -> None:
        """Add a Note object to the index using the given writer. If the
        filepath already exists in the index an update will be performed instead."""
        writer.update_document(
            filename=note.filename,
            last_modified=note.last_modified,
            title=note.title,
            content=note.content,
        )

    def get_notes(self) -> List[Note]:
        """Return a list containing a Note object for every file in the notes directory."""
        return [
            Note(self, os.path.split(filepath)[1])
            for filepath in glob.glob(os.path.join(self.dir, "*.md"))
        ]

    def update_index(self, clean: bool = False) -> None:
        """Synchronize the index with the notes directory.
        Specify clean=True to completely rebuild the index"""
        indexed = set()
        writer = self.index.writer()
        if clean:
            writer.mergetype = writing.CLEAR  # Clear the index
        with self.index.searcher() as searcher:
            for idx_note in searcher.all_stored_fields():
                idx_filename = idx_note["filename"]
                idx_filepath = os.path.join(self.dir, idx_filename)
                # Delete missing
                if not os.path.exists(idx_filepath):
                    writer.delete_by_term("filename", idx_filename)
                    logging.debug(f"'{idx_filename}' removed from index")
                # Update modified
                elif (
                    os.path.getmtime(idx_filepath) != idx_note["last_modified"]
                ):
                    logging.debug(f"'{idx_filename}' updated")
                    self._add_note_to_index(writer, Note(self, idx_filename))
                    indexed.add(idx_filename)
                # Ignore already indexed
                else:
                    indexed.add(idx_filename)
        # Add new
        for note in self.get_notes():
            if note.filename not in indexed:
                self._add_note_to_index(writer, note)
                logging.debug(f"'{note.filename}' added to index")
        writer.commit()
        self.last_index_update = datetime.now()

    def update_index_debounced(self, clean: bool = False) -> None:
        """Run update_index() but only if it hasn't been run in the last 10 seconds."""
        if (
            self.last_index_update is None
            or (datetime.now() - self.last_index_update).seconds > 10
        ):
            self.update_index(clean=clean)

    def search(self, term: str) -> Tuple[NoteHit]:
        """Search the index for the given term."""
        self.update_index_debounced()
        with self.index.searcher() as searcher:
            query = MultifieldParser(
                ["title", "content"], self.index.schema
            ).parse(term)
            results = searcher.search(query)
            return tuple(NoteHit(self, hit) for hit in results)
