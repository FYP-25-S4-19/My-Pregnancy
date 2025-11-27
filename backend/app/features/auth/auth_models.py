from datetime import date

from app.core.custom_base_model import CustomBaseModel


class CreatePregAccountRequest(CustomBaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str
    password: str
    due_date: date | None = None


class AuthLoginRequest(CustomBaseModel):
    email: str
    password: str


class AuthLoginResponse(CustomBaseModel):
    access_token: str
    token_type: str
