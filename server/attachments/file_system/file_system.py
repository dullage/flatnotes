import os
import shutil

from fastapi import UploadFile
from fastapi.responses import FileResponse

from helpers import get_env, is_valid_filename

from ..base import BaseAttachments


class FileSystemAttachments(BaseAttachments):
    def __init__(self):
        self.base_path = get_env("FLATNOTES_PATH", mandatory=True)
        if not os.path.exists(self.base_path):
            raise NotADirectoryError(
                f"'{self.base_path}' is not a valid directory."
            )
        self.storage_path = os.path.join(self.base_path, "attachments")
        os.makedirs(self.storage_path, exist_ok=True)

    def create(self, file: UploadFile) -> None:
        """Create a new attachment."""
        is_valid_filename(file.filename)
        filepath = os.path.join(self.storage_path, file.filename)
        if os.path.exists(filepath):
            raise FileExistsError(f"'{file.filename}' already exists.")
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)

    def get(self, filename: str) -> FileResponse:
        """Get a specific attachment."""
        is_valid_filename(filename)
        filepath = os.path.join(self.storage_path, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"'{filename}' not found.")
        return FileResponse(filepath)
