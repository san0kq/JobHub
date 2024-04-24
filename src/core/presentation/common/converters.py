from typing import Any, TypeVar

from dacite import from_dict

T = TypeVar('T')


def convert_data_from_request_to_dto(
    dto: type[T], data_from_form: dict[str, Any]
) -> T:
    """
    Convert data from a request to a DTO object.

    Args:
        dto (type[T]): The DTO class type.
        data_from_form (dict[str, Any]): The data from the form.

    Returns:
        T: The DTO object.
    """
    return from_dict(dto, data_from_form)
