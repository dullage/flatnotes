from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Request

from .models import Login, Token


class BaseAuth(ABC):
    @abstractmethod
    def login(self, data: Login) -> Token:
        """Login a user."""
        pass

    @abstractmethod
    def authenticate(self, token: str) -> bool:
        """Authenticate a user."""
        pass

    async def get_authorization_url(self, request: Request) -> Optional[str]:
        return None

    async def handle_callback(self, request: Request) -> Optional[Token]:
        return None
