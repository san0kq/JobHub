from dataclasses import dataclass
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class ProfileEditDTO:
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    phone: Optional[str]
    avatar: InMemoryUploadedFile | bool | None
