from datetime import date

from app.core.custom_base_model import CustomBaseModel


class CreatePregAccountRequest(CustomBaseModel):
    username: str
    email: str
    password: str
    due_date: date | None


class AuthLoginRequest(CustomBaseModel):
    username: str
    password: str


class AuthLoginResponse(CustomBaseModel):
    access_token: str
    token_type: str
