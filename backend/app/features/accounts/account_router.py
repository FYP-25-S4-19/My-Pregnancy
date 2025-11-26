from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.db_config import get_db
from app.features.accounts.account_service import AccountService

account_router = APIRouter(prefix="/accounts", tags=["Account"])


def get_account_service(db: Session = Depends(get_db)) -> AccountService:
    return AccountService(db)


@account_router.post("/create-account", status_code=status.HTTP_201_CREATED)
def create_account(
    email: str,
    password: str,
    service: AccountService = Depends(get_account_service),
) -> None:
    pass  # Implementation for account creation goes here
