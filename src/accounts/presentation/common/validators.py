from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.core.files import File

from django.core.exceptions import ValidationError


class ValidateMinAge:
    """
    Validator class to ensure the provided date meets a minimum age requirement.

    Args:
        min_age (int): The minimum age required in years.

    Raises:
        ValidationError: If the provided date does not meet the minimum age requirement.
    """

    def __init__(self, min_age: int) -> None:
        self._min_age = min_age

    def __call__(self, date: date) -> Any:
        age = (date.today() - date).days / 365
        if self._min_age > age:
            raise ValidationError(
                f'The minimum allowable age is {self._min_age} years.'
            )


class ValidateMaxAge:
    """
    Validator class to ensure the provided date does not exceed a maximum age.

    Args:
        max_age (int): The maximum age allowed in years.

    Raises:
        ValidationError: If the provided date exceeds the maximum age.
    """

    def __init__(self, max_age: int) -> None:
        self._max_age = max_age

    def __call__(self, date: date) -> Any:
        age = (date.today() - date).days / 365
        if self._max_age < age:
            raise ValidationError(
                f'The maximum allowable age is {self._max_age} years.'
            )


class ValidateFileExtension:
    """
    Validator class to ensure the uploaded file has an allowed extension.

    Args:
        available_extensions (list[str]): List of allowed file extensions.

    Raises:
        ValidationError: If the uploaded file has an invalid extension.
    """

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, file: File) -> None:
        if '.' not in file.name:
            raise ValidationError(message='File must have extension.')
        file_extension = file.name.split(".")[-1]
        if file_extension not in self._available_extensions:
            raise ValidationError(
                message=f'Accept only {self._available_extensions}'
            )


class ValidateFileSize:
    """
    Validator class to ensure the uploaded file does not exceed a maximum size.

    Args:
        max_size (int): The maximum allowed file size in bytes.

    Raises:
        ValidationError: If the uploaded file exceeds the maximum size.
    """

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, file: File) -> None:
        if file.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(
                message=f'Max file size is {max_size_in_mb} MB'
            )


def validate_username(username: str) -> None:
    """
    Validator function to ensure the username does not contain the @ symbol.

    Args:
        username (str): The username to be validated.

    Raises:
        ValidationError: If the username contains the @ symbol.
    """
    if '@' in username:
        raise ValidationError(
            message='Username should not contain the @ symbol'
        )
