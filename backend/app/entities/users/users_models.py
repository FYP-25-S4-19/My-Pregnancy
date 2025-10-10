from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=10, max_length=64)
    password: str = Field()


class CreateUserResponse(CreateUserRequest):
    id: int
