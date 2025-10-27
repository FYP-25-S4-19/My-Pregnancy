from app.features.users.user_models import CreateUserRequest
from app.core.security import require_role, bearer_scheme
from fastapi import APIRouter, Depends
from app.db.db_schema import User

users_router = APIRouter(prefix="/api/users")


@users_router.get("/")
def get_all_users(
    user: User = Depends(require_role("Admin"))
) -> str:
    return f"Admin with user ID '{user.id}' is retrieving all users"


@users_router.post("/")
def create_user(req: CreateUserRequest) -> str:
    return "TODO: Return a person object"
