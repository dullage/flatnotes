import glob
import logging
import os
import re
from datetime import datetime
from typing import List, Tuple

import whoosh
from helpers import empty_dir, re_extract, strip_ext
from whoosh import writing
from whoosh.analysis import CharsetFilter, KeywordAnalyzer, StemmingAnalyzer
from whoosh.fields import ID, STORED, TEXT, SchemaClass
from whoosh.index import Index
from whoosh.qparser import MultifieldParser
from whoosh.searching import Hit
from whoosh.support.charset import accent_map

MARKDOWN_EXT = ".md"
INDEX_SCHEMA_VERSION = "3"
TAG_TOKEN_REGEX = re.compile(r"(?:(?<=^#)|(?<=\s#))\w+(?=\s|$)")

StemmingFoldingAnalyzer = StemmingAnalyzer() | CharsetFilter(accent_map)


class IndexSchema(SchemaClass):
    filename = ID(unique=True, stored=True)
    last_modified = STORED()
    title = TEXT(field_boost=2, analyzer=StemmingFoldingAnalyzer)
    content = TEXT(analyzer=StemmingFoldingAnalyzer)
    tags = TEXT(analyzer=KeywordAnalyzer(lowercase=True))


class InvalidTitleError(Exception):
    def __init__(self, message="The specified title is invalid"):
        self.message = message
        super().__init__(self.message)


class Note:
    def __init__(
        self, flatnotes: "Flatnotes", title: str, new: bool = False
    ) -> None:
        self._flatnotes = flatnotes
        self._title = title.strip()
        if not self._is_valid_title(self._title):
            raise InvalidTitleError
        if new and os.path.exists(self.filepath):
            raise FileExistsError
        elif new:
            open(self.filepath, "w").close()

    @property
    def filepath(self):
        return os.path.join(self._flatnotes.dir, self.filename)

    @property
    def filename(self):
        return self._title + MARKDOWN_EXT

    @property
    def last_modified(self):
        return os.path.getmtime(self.filepath)

    # Editable Properties
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if not self._is_valid_title(new_title):
            raise InvalidTitleError
        new_filepath = os.path.join(
            self._flatnotes.dir, new_title + MARKDOWN_EXT
        )
        os.rename(self.filepath, new_filepath)
        self._title = new_title

    @property
    def content(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.read()

    @content.setter
    def content(self, new_content):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    def delete(self):
        os.remove(self.filepath)

    # Functions
    def _is_valid_title(self, title: str) -> bool:
        r"""Return False if the declared title contains any of the following
        characters: <>:"/\|?*"""
        invalid_chars = r'<>:"/\|?*'
        return not any(invalid_char in title for invalid_char in invalid_chars)


class NoteHit(Note):
    def __init__(self, flatnotes: "Flatnotes", hit: Hit) -> None:
        super().__init__(flatnotes, strip_ext(hit["filename"]))
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
        index_dir_exists = os.path.exists(self.index_dir)
        if index_dir_exists and whoosh.index.exists_in(
            self.index_dir, indexname=INDEX_SCHEMA_VERSION
        ):
            logging.info("Loading existing index")
            return whoosh.index.open_dir(
                self.index_dir, indexname=INDEX_SCHEMA_VERSION
            )
        else:
            if index_dir_exists:
                logging.info("Deleting outdated index")
                empty_dir(self.index_dir)
            else:
                os.mkdir(self.index_dir)
            logging.info("Creating new index")
            return whoosh.index.create_in(
                self.index_dir, IndexSchema, indexname=INDEX_SCHEMA_VERSION
            )

    def _add_note_to_index(
        self, writer: writing.IndexWriter, note: Note
    ) -> None:
        """Add a Note object to the index using the given writer. If the
        filename already exists in the index an update will be performed
        instead."""
        content, tag_list = re_extract(TAG_TOKEN_REGEX, note.content)
        writer.update_document(
            filename=note.filename,
            last_modified=note.last_modified,
            title=note.title,
            content=content,
            tags=" ".join(tag_list),
        )

    def get_notes(self) -> List[Note]:
        """Return a list containing a Note object for every file in the notes
        directory."""
        return [
            Note(self, strip_ext(os.path.split(filepath)[1]))
            for filepath in glob.glob(
                os.path.join(self.dir, "*" + MARKDOWN_EXT)
            )
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
                    logging.info(f"'{idx_filename}' removed from index")
                # Update modified
                elif (
                    os.path.getmtime(idx_filepath) != idx_note["last_modified"]
                ):
                    logging.info(f"'{idx_filename}' updated")
                    self._add_note_to_index(
                        writer, Note(self, strip_ext(idx_filename))
                    )
                    indexed.add(idx_filename)
                # Ignore already indexed
                else:
                    indexed.add(idx_filename)
        # Add new
        for note in self.get_notes():
            if note.filename not in indexed:
                self._add_note_to_index(writer, note)
                logging.info(f"'{note.filename}' added to index")
        writer.commit()
        self.last_index_update = datetime.now()

    def update_index_debounced(self, clean: bool = False) -> None:
        """Run update_index() but only if it hasn't been run in the last 10
        seconds."""
        if (
            self.last_index_update is None
            or (datetime.now() - self.last_index_update).seconds > 10
        ):
            self.update_index(clean=clean)

    def search(self, term: str) -> Tuple[NoteHit, ...]:
        """Search the index for the given term."""
        self.update_index_debounced()
        with self.index.searcher() as searcher:
            query = MultifieldParser(
                ["title", "content", "tags"], self.index.schema
            ).parse(term)
            results = searcher.search(query, limit=None)
            return tuple(NoteHit(self, hit) for hit in results)
