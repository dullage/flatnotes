import os
import secrets
import shutil
from typing import List, Literal, Union

import pyotp
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from qrcode import QRCode

from auth import create_access_token, no_auth, validate_token
from config import AuthType, config
from error_responses import (
    filename_exists_response,
    invalid_filename_response,
    note_not_found_response,
)
from flatnotes import Flatnotes, InvalidTitleError, Note
from helpers import is_valid_filename
from models import (
    ConfigModel,
    LoginModel,
    NoteContentResponseModel,
    NotePatchModel,
    NotePostModel,
    NoteResponseModel,
    SearchResultModel,
    TokenModel,
)

ATTACHMENTS_DIR = os.path.join(config.data_path, "attachments")
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

app = FastAPI()
flatnotes = Flatnotes(config.data_path)

totp = (
    pyotp.TOTP(config.totp_key) if config.auth_type == AuthType.TOTP else None
)
last_used_totp = None

if config.auth_type in [AuthType.NONE, AuthType.READ_ONLY]:
    authenticate = no_auth
else:
    authenticate = validate_token

# Display TOTP QR code
if config.auth_type == AuthType.TOTP:
    uri = totp.provisioning_uri(issuer_name="flatnotes", name=config.username)
    qr = QRCode()
    qr.add_data(uri)
    print(
        "\nScan this QR code with your TOTP app of choice",
        "e.g. Authy or Google Authenticator:",
    )
    qr.print_ascii()
    print(f"Or manually enter this key: {totp.secret.decode('utf-8')}\n")

if config.auth_type not in [AuthType.NONE, AuthType.READ_ONLY]:

    @app.post("/api/token", response_model=TokenModel)
    def token(data: LoginModel):
        global last_used_totp

        username_correct = secrets.compare_digest(
            config.username.lower(), data.username.lower()
        )

        expected_password = config.password
        if config.auth_type == AuthType.TOTP:
            current_totp = totp.now()
            expected_password += current_totp
        password_correct = secrets.compare_digest(
            expected_password, data.password
        )

        if not (
            username_correct
            and password_correct
            # Prevent TOTP from being reused
            and (
                config.auth_type != AuthType.TOTP
                or current_totp != last_used_totp
            )
        ):
            raise HTTPException(
                status_code=400, detail="Incorrect login credentials."
            )

        access_token = create_access_token(data={"sub": config.username})
        if config.auth_type == AuthType.TOTP:
            last_used_totp = current_totp
        return TokenModel(access_token=access_token)


@app.get("/", include_in_schema=False)
@app.get("/login", include_in_schema=False)
@app.get("/search", include_in_schema=False)
@app.get("/new", include_in_schema=False)
@app.get("/note/{title}", include_in_schema=False)
def root(title: str = ""):
    with open("client/dist/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


if config.auth_type != AuthType.READ_ONLY:

    @app.post(
        "/api/notes",
        dependencies=[Depends(authenticate)],
        response_model=NoteContentResponseModel,
    )
    def post_note(data: NotePostModel):
        """Create a new note."""
        try:
            note = Note(flatnotes, data.title, new=True)
            note.content = data.content
            return NoteContentResponseModel.model_validate(note)
        except InvalidTitleError:
            return invalid_filename_response
        except FileExistsError:
            return filename_exists_response


@app.get(
    "/api/notes/{title}",
    dependencies=[Depends(authenticate)],
    response_model=Union[NoteContentResponseModel, NoteResponseModel],
)
def get_note(
    title: str,
    include_content: bool = True,
):
    """Get a specific note."""
    try:
        note = Note(flatnotes, title)
        if include_content:
            return NoteContentResponseModel.model_validate(note)
        else:
            return NoteResponseModel.model_validate(note)
    except InvalidTitleError:
        return invalid_filename_response
    except FileNotFoundError:
        return note_not_found_response


if config.auth_type != AuthType.READ_ONLY:

    @app.patch(
        "/api/notes/{title}",
        dependencies=[Depends(authenticate)],
        response_model=NoteContentResponseModel,
    )
    def patch_note(title: str, new_data: NotePatchModel):
        try:
            note = Note(flatnotes, title)
            if new_data.new_title is not None:
                note.title = new_data.new_title
            if new_data.new_content is not None:
                note.content = new_data.new_content
            return NoteContentResponseModel.model_validate(note)
        except InvalidTitleError:
            return invalid_filename_response
        except FileExistsError:
            return filename_exists_response
        except FileNotFoundError:
            return note_not_found_response


if config.auth_type != AuthType.READ_ONLY:

    @app.delete(
        "/api/notes/{title}",
        dependencies=[Depends(authenticate)],
        response_model=None,
    )
    def delete_note(title: str):
        try:
            note = Note(flatnotes, title)
            note.delete()
        except InvalidTitleError:
            return invalid_filename_response
        except FileNotFoundError:
            return note_not_found_response


@app.get(
    "/api/tags",
    dependencies=[Depends(authenticate)],
    response_model=List[str],
)
def get_tags():
    """Get a list of all indexed tags."""
    return flatnotes.get_tags()


@app.get(
    "/api/search",
    dependencies=[Depends(authenticate)],
    response_model=List[SearchResultModel],
)
def search(
    term: str,
    sort: Literal["score", "title", "lastModified"] = "score",
    order: Literal["asc", "desc"] = "desc",
    limit: int = None,
):
    """Perform a full text search on all notes."""
    if sort == "lastModified":
        sort = "last_modified"
    return [
        SearchResultModel.model_validate(note_hit)
        for note_hit in flatnotes.search(
            term, sort=sort, order=order, limit=limit
        )
    ]


@app.get("/api/config", response_model=ConfigModel)
def get_config():
    """Retrieve server-side config required for the UI."""
    return ConfigModel.model_validate(config)


if config.auth_type != AuthType.READ_ONLY:

    @app.post(
        "/api/attachments",
        dependencies=[Depends(authenticate)],
        response_model=None,
    )
    def post_attachment(file: UploadFile):
        """Upload an attachment."""
        if not is_valid_filename(file.filename):
            return invalid_filename_response
        filepath = os.path.join(ATTACHMENTS_DIR, file.filename)
        if os.path.exists(filepath):
            return filename_exists_response
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)


@app.get(
    "/attachments/{filename}",
    dependencies=[Depends(authenticate)],
    include_in_schema=False,
)
def get_attachment(filename: str):
    """Download an attachment."""
    if not is_valid_filename(filename):
        raise HTTPException(status_code=400, detail="Invalid filename.")
    filepath = os.path.join(ATTACHMENTS_DIR, filename)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(filepath)


app.mount("/", StaticFiles(directory="client/dist"), name="dist")
