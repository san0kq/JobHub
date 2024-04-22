from dataclasses import dataclass


@dataclass
class LoginDTO:
    email_or_username: str
    password: str
