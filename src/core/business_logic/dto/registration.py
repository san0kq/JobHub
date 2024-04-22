from dataclasses import dataclass
from datetime import date


@dataclass
class RegistrationDTO:
    email: str
    username: str
    date_of_birth: date
    password: str
