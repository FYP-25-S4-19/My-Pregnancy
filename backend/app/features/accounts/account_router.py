from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import Admin
from app.features.accounts.account_service import AccountService

account_router = APIRouter(prefix="/accounts", tags=["Account"])


def get_account_service(db: AsyncSession = Depends(get_db)) -> AccountService:
    return AccountService(db)


@account_router.post("/requests/doctor/", status_code=status.HTTP_201_CREATED)
async def submit_doctor_account_creation_request(
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    middle_name: str | None = Form(None),
    last_name: str = Form(...),
    qualification_option: str = Form(...),
    qualification_img: UploadFile = File(),
    service: AccountService = Depends(get_account_service),
    db: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.submit_doctor_account_creation_request(
            email,
            password,
            first_name,
            middle_name,
            last_name,
            qualification_option,
            qualification_img,
        )
        await db.commit()
    except:
        await db.rollback()
        raise


@account_router.get("/requests/")
async def get_account_creation_requests(
    _: Admin = Depends(require_role(Admin)), service: AccountService = Depends(get_account_service)
):
    return service.get_account_creation_requests()


@account_router.patch("/requests/accept/{request_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def accept_account_creation_request(
    request_id: int,
    _: Admin = Depends(require_role(Admin)),
    service: AccountService = Depends(get_account_service),
    db: AsyncSession = Depends(get_db),
):
    try:
        await service.accept_account_creation_request(request_id)
        await db.commit()
    except:
        await db.rollback()
        raise


@account_router.patch("/requests/reject/{request_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def reject_account_creation_request(
    request_id: int,
    _: Admin = Depends(require_role(Admin)),
    service: AccountService = Depends(get_account_service),
    db: AsyncSession = Depends(get_db),
):
    try:
        await service.reject_account_creation_request(request_id)
        await db.commit()
    except:
        await db.rollback()
        raise
