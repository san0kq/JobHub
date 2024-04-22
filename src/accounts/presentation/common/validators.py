from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.core.files import File

from django.core.exceptions import ValidationError


class ValidateMinAge:
    """
    Age validation.

    The minimum age is set during the class initialization.

    The data from the form is passed to the __call__ method.
    """

    def __init__(self, min_age: int) -> None:
        self._min_age = min_age

    def __call__(self, date: date) -> Any:
        age = (date.today() - date).days / 365
        if self._min_age > age:
            raise ValidationError(
                f"The minimum allowable age is {self._min_age} years."
            )


class ValidateMaxAge:
    """
    Age validation.

    The maximum age is set during the class initialization.

    The data from the form is passed to the __call__ method.
    """

    def __init__(self, max_age: int) -> None:
        self._max_age = max_age

    def __call__(self, date: date) -> Any:
        age = (date.today() - date).days / 365
        if self._max_age < age:
            raise ValidationError(
                f"The maximum allowable age is {self._max_age} years."
            )


class ValidateFileExtension:
    """
    File extension validation.

    The list of allowed extensions is passed during class initialization.
    """

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, file: File) -> None:
        if "." not in file.name:
            raise ValidationError(message="File must have extension.")
        file_extension = file.name.split(".")[-1]
        if file_extension not in self._available_extensions:
            raise ValidationError(
                message=f"Accept only {self._available_extensions}"
            )


class ValidateFileSize:
    """
    File size validation.

    The maximum allowable value is passed during class initialization in bytes.
    """

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, file: File) -> None:
        if file.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(
                message=f"Max file size is {max_size_in_mb} MB"
            )


def validate_username(username: str) -> None:
    if "@" in username:
        raise ValidationError(
            message="Username should not contain the @ symbol"
        )
