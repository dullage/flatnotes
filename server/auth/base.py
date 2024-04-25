from abc import ABC, abstractmethod

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
