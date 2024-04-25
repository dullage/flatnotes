from abc import ABC, abstractmethod

from fastapi import UploadFile
from fastapi.responses import FileResponse

from .models import AttachmentCreateResponse


class BaseAttachments(ABC):
    @abstractmethod
    def create(self, file: UploadFile) -> AttachmentCreateResponse:
        """Create a new attachment."""
        pass

    @abstractmethod
    def get(self, filename: str) -> FileResponse:
        """Get a specific attachment."""
        pass
