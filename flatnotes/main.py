import logging
import os
from typing import List, Literal

from auth import (
    FLATNOTES_PASSWORD,
    FLATNOTES_USERNAME,
    create_access_token,
    validate_token,
)
from error_responses import (
    title_exists_response,
    note_not_found_response,
    invalid_title_response,
)
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import LoginModel, NoteHitModel, NoteModel, NotePatchModel

from flatnotes import Flatnotes, InvalidTitleError, Note

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())

app = FastAPI()
flatnotes = Flatnotes(os.environ["FLATNOTES_PATH"])


@app.post("/api/token")
async def token(data: LoginModel):
    if (
        data.username != FLATNOTES_USERNAME
        or data.password != FLATNOTES_PASSWORD
    ):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": FLATNOTES_USERNAME})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
@app.get("/login")
@app.get("/search")
@app.get("/new")
@app.get("/note/{title}")
async def root(title: str = ""):
    with open("flatnotes/dist/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/api/notes", response_model=List[NoteModel])
async def get_notes(
    start: int = 0,
    limit: int = None,
    sort: Literal["title", "lastModified"] = "title",
    order: Literal["asc", "desc"] = "asc",
    include_content: bool = False,
    _: str = Depends(validate_token),
):
    """Get all notes."""
    notes = flatnotes.get_notes()
    notes.sort(
        key=lambda note: note.last_modified
        if sort == "lastModified"
        else note.title,
        reverse=order == "desc",
    )
    return [
        NoteModel.dump(note, include_content=include_content)
        for note in notes[start : None if limit is None else start + limit]
    ]


@app.post("/api/notes", response_model=NoteModel)
async def post_note(data: NoteModel, _: str = Depends(validate_token)):
    """Create a new note."""
    try:
        note = Note(flatnotes, data.title, new=True)
        note.content = data.content
        return NoteModel.dump(note, include_content=True)
    except InvalidTitleError:
        return invalid_title_response
    except FileExistsError:
        return title_exists_response


@app.get("/api/notes/{title}", response_model=NoteModel)
async def get_note(
    title: str,
    include_content: bool = True,
    _: str = Depends(validate_token),
):
    """Get a specific note."""
    try:
        note = Note(flatnotes, title)
        return NoteModel.dump(note, include_content=include_content)
    except InvalidTitleError:
        return invalid_title_response
    except FileNotFoundError:
        return note_not_found_response


@app.patch("/api/notes/{title}", response_model=NoteModel)
async def patch_note(
    title: str, new_data: NotePatchModel, _: str = Depends(validate_token)
):
    try:
        note = Note(flatnotes, title)
        if new_data.new_title is not None:
            note.title = new_data.new_title
        if new_data.new_content is not None:
            note.content = new_data.new_content
        return NoteModel.dump(note, include_content=True)
    except InvalidTitleError:
        return invalid_title_response
    except FileExistsError:
        return title_exists_response
    except FileNotFoundError:
        return note_not_found_response


@app.delete("/api/notes/{title}")
async def delete_note(title: str, _: str = Depends(validate_token)):
    try:
        note = Note(flatnotes, title)
        note.delete()
    except InvalidTitleError:
        return invalid_title_response
    except FileNotFoundError:
        return note_not_found_response


@app.get("/api/search", response_model=List[NoteHitModel])
async def search(term: str, _: str = Depends(validate_token)):
    """Perform a full text search for a note."""
    return [NoteHitModel.dump(note_hit) for note_hit in flatnotes.search(term)]


app.mount("/", StaticFiles(directory="flatnotes/dist"), name="dist")
