import glob
import logging
import os
from datetime import datetime
from typing import List, Tuple

import whoosh
from whoosh import writing
from whoosh.fields import ID, STORED, TEXT, SchemaClass
from whoosh.index import Index
from whoosh.qparser import MultifieldParser
from whoosh.searching import Hit


class IndexSchema(SchemaClass):
    filepath = ID(unique=True, stored=True)
    last_modified = STORED()
    title = TEXT(field_boost=2)
    content = TEXT()


class Note:
    def __init__(self, filepath: str, new: bool = False) -> None:
        if new and os.path.exists(filepath):
            raise FileExistsError
        elif new:
            open(filepath, "w").close()
        self._filepath = filepath

    @property
    def filepath(self):
        return self._filepath

    @property
    def dirpath(self):
        return os.path.split(self._filepath)[0]

    @property
    def title(self):
        return os.path.splitext(self.filename)[0]

    @property
    def last_modified(self):
        return os.path.getmtime(self._filepath)

    # Editable Properties
    @property
    def filename(self):
        return os.path.split(self._filepath)[1]

    @filename.setter
    def filename(self, new_filename):
        new_filepath = os.path.join(self.dirpath, new_filename)
        os.rename(self._filepath, new_filepath)
        self._filepath = new_filepath

    @property
    def content(self):
        with open(self._filepath, "r") as f:
            return f.read()

    @content.setter
    def content(self, new_content):
        if not os.path.exists(self._filepath):
            raise FileNotFoundError
        with open(self._filepath, "w") as f:
            f.write(new_content)

    def delete(self):
        os.remove(self._filepath)


class NoteHit(Note):
    def __init__(self, hit: Hit) -> None:
        self.filepath = hit["filepath"]
        self.title_highlights = hit.highlights("title", text=self.title)
        self.content_highlights = hit.highlights(
            "content",
            text=self.content,
        )


class Flatnotes(object):
    def __init__(self, notes_dirpath: str) -> None:
        if not os.path.exists(notes_dirpath):
            raise NotADirectoryError(
                f"'{notes_dirpath}' is not a valid directory."
            )
        self.notes_dirpath = notes_dirpath

        self.index = self._load_index()
        self.last_index_update = None
        self.update_index()

    @property
    def index_dirpath(self):
        return os.path.join(self.notes_dirpath, ".flatnotes")

    def _load_index(self) -> Index:
        """Load the note index or create new if not exists."""
        if not os.path.exists(self.index_dirpath):
            os.mkdir(self.index_dirpath)
        if whoosh.index.exists_in(self.index_dirpath):
            logging.info("Existing index loaded")
            return whoosh.index.open_dir(self.index_dirpath)
        else:
            logging.info("New index created")
            return whoosh.index.create_in(self.index_dirpath, IndexSchema)

    def _add_note_to_index(
        self, writer: writing.IndexWriter, note: Note
    ) -> None:
        """Add a Note object to the index using the given writer. If the
        filepath already exists in the index an update will be performed instead."""
        writer.update_document(
            filepath=note.filepath,
            last_modified=note.last_modified,
            title=note.title,
            content=note.content,
        )

    def get_notes(self) -> List[Note]:
        """Return a list containing a Note object for every file in the notes directory."""
        return [
            Note(filepath)
            for filepath in glob.glob(os.path.join(self.notes_dirpath, "*.md"))
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
                idx_filepath = idx_note["filepath"]
                # Delete missing
                if not os.path.exists(idx_filepath):
                    writer.delete_by_term("filepath", idx_filepath)
                    logging.debug(f"{idx_filepath} removed from index")
                # Update modified
                elif (
                    os.path.getmtime(idx_filepath) != idx_note["last_modified"]
                ):
                    logging.debug(f"{idx_filepath} updated")
                    self._add_note_to_index(writer, Note(idx_filepath))
                    indexed.add(idx_filepath)
                # Ignore already indexed
                else:
                    indexed.add(idx_filepath)
        # Add new
        for note in self.get_notes():
            if note.filepath not in indexed:
                self._add_note_to_index(writer, note)
                logging.debug(f"{note.filepath} added to index")
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
            return tuple(NoteHit(result) for result in results)
