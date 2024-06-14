import os
import shutil
import urllib.parse
from datetime import datetime

from fastapi import UploadFile
from fastapi.responses import FileResponse

from helpers import get_env, is_valid_filename

from ..base import BaseAttachments
from ..models import AttachmentCreateResponse


class FileSystemAttachments(BaseAttachments):
    def __init__(self):
        self.base_path = get_env("FLATNOTES_PATH", mandatory=True)
        if not os.path.exists(self.base_path):
            raise NotADirectoryError(
                f"'{self.base_path}' is not a valid directory."
            )
        self.storage_path = os.path.join(self.base_path, "attachments")
        os.makedirs(self.storage_path, exist_ok=True)

    def create(self, file: UploadFile) -> AttachmentCreateResponse:
        """Create a new attachment."""
        is_valid_filename(file.filename)
        try:
            self._save_file(file)
        except FileExistsError:
            file.filename = self._datetime_suffix_filename(file.filename)
            self._save_file(file)
        return AttachmentCreateResponse(
            filename=file.filename, url=self._url_for_filename(file.filename)
        )

    def get(self, filename: str) -> FileResponse:
        """Get a specific attachment."""
        is_valid_filename(filename)
        filepath = os.path.join(self.storage_path, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"'{filename}' not found.")
        return FileResponse(filepath)

    def _save_file(self, file: UploadFile):
        filepath = os.path.join(self.storage_path, file.filename)
        with open(filepath, "xb") as f:
            shutil.copyfileobj(file.file, f)

    def _datetime_suffix_filename(self, filename: str) -> str:
        """Add a timestamp suffix to the filename."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
        name, ext = os.path.splitext(filename)
        return f"{name}_{timestamp}{ext}"

    def _url_for_filename(self, filename: str) -> str:
        """Return the URL for the given filename."""
        return f"attachments/{urllib.parse.quote(filename)}"
