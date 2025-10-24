from fastapi import APIRouter

from app.features.users.user_models import CreateUserRequest

users_router = APIRouter(prefix="/api/users")


@users_router.get("/")
def get_all_users() -> str:
    return "Getting all educational-articles"


@users_router.post("/")
def create_user(req: CreateUserRequest) -> str:
    return "TODO: Return a person object"
