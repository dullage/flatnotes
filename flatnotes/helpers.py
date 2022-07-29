import os

from pydantic import BaseModel


def strip_ext(filename):
    return os.path.splitext(filename)[0]


def camel_case(snake_case_str: str) -> str:
    """Return the declared snake_case string in camelCase."""
    parts = [part for part in snake_case_str.split("_") if part != ""]
    return parts[0] + "".join(part.title() for part in parts[1:])


class CamelCaseBaseModel(BaseModel):
    class Config:
        alias_generator = camel_case
