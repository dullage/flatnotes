import logging
import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from flatnotes import Flatnotes

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())

app = FastAPI()

flatnotes = Flatnotes(os.environ["FLATNOTES_PATH"])


@app.get("/")
async def root():
    return RedirectResponse("/index.html")


@app.get("/api/notes")
async def notes():
    return [
        {"filename": note.filename, "lastModified": note.last_modified}
        for note in flatnotes.get_notes()
    ]


@app.get("/api/search")
async def search(term: str):
    return [
        {
            "filename": hit.filename,
            "lastModified": hit.last_modified,
            "titleHighlights": hit.title_highlights,
            "contentHighlights": hit.content_highlights,
        }
        for hit in flatnotes.search(term)
    ]


app.mount("/", StaticFiles(directory="flatnotes/dist"), name="dist")
