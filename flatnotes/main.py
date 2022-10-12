import secrets
from typing import List, Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from auth import create_access_token, validate_token
from config import config
from error_responses import (
    invalid_title_response,
    note_not_found_response,
    title_exists_response,
)
from flatnotes import Flatnotes, InvalidTitleError, Note
from models import (
    ConfigModel,
    LoginModel,
    NoteModel,
    NotePatchModel,
    SearchResultModel,
)

app = FastAPI()
flatnotes = Flatnotes(config.data_path)


@app.post("/api/token")
async def token(data: LoginModel):
    username_correct = secrets.compare_digest(
        config.username.lower(), data.username.lower()
    )
    password_correct = secrets.compare_digest(config.password, data.password)
    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": config.username})
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


@app.get("/api/tags")
async def get_tags(_: str = Depends(validate_token)):
    """Get a list of all indexed tags."""
    return flatnotes.get_tags()


@app.get("/api/search", response_model=List[SearchResultModel])
async def search(
    term: str,
    sort: Literal["score", "title", "lastModified"] = "score",
    order: Literal["asc", "desc"] = "desc",
    limit: int = None,
    _: str = Depends(validate_token),
):
    """Perform a full text search on all notes."""
    if sort == "lastModified":
        sort = "last_modified"
    return [
        SearchResultModel.dump(note_hit)
        for note_hit in flatnotes.search(
            term, sort=sort, order=order, limit=limit
        )
    ]


@app.get("/api/config", response_model=ConfigModel)
async def get_config():
    """Retrieve server-side config required for the UI."""
    return ConfigModel.dump(config)


app.mount("/", StaticFiles(directory="flatnotes/dist"), name="dist")
