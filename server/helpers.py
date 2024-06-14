import os
import re
import sys

from pydantic import BaseModel

from logger import logger


def camel_case(snake_case_str: str) -> str:
    """Return the declared snake_case string in camelCase."""
    parts = [part for part in snake_case_str.split("_") if part != ""]
    return parts[0] + "".join(part.title() for part in parts[1:])


def is_valid_filename(value):
    """Raise ValueError if the declared string contains any of the following
    characters: <>:"/\\|?*"""
    invalid_chars = r'<>:"/\|?*'
    if any(invalid_char in value for invalid_char in invalid_chars):
        raise ValueError(
            "title cannot include any of the following characters: "
            + invalid_chars
        )
    return value


def strip_whitespace(value):
    """Return the declared string with leading and trailing whitespace
    removed."""
    return value.strip()


def get_env(
    key, mandatory=False, default=None, cast_int=False, cast_bool=False
):
    """Get an environment variable. If `mandatory` is True and environment
    variable isn't set, exit the program"""
    value = os.environ.get(key)
    if mandatory and not value:
        logger.error(f"Environment variable {key} must be set.")
        sys.exit(1)
    if not mandatory and not value:
        return default
    if cast_int:
        try:
            value = int(value)
        except (TypeError, ValueError):
            logger.error(f"Invalid value '{value}' for {key}.")
            sys.exit(1)
    if cast_bool:
        value = value.lower()
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            logger.error(f"Invalid value '{value}' for {key}.")
            sys.exit(1)
    return value


def replace_base_href(html_file, path_prefix):
    """Replace the href value for the base element in an HTML file."""
    base_path = path_prefix + "/"
    logger.info(
        f"Replacing href value for base element in '{html_file}' "
        + f"with '{base_path}'."
    )
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()
    pattern = r'(<base\s+href=")[^"]*(")'
    replacement = r"\1" + base_path + r"\2"
    updated_html = re.sub(pattern, replacement, html, flags=re.IGNORECASE)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_html)


class CustomBaseModel(BaseModel):
    class Config:
        alias_generator = camel_case
        populate_by_name = True
        from_attributes = True
