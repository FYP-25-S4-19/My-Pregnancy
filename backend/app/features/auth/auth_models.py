from pydantic import BaseModel


class AuthLoginRequest(BaseModel):
    email: str
    password: str


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str
