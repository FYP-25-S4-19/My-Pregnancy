from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_schema import DoctorAccountCreationRequest, DoctorQualificationOption, VolunteerDoctor


class AccountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_doctor_account_creation_request(
        self,
        email: str,
        password: str,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        qualification_option: str,
        qualification_img: UploadFile,
    ) -> None:
        if qualification_option not in DoctorQualificationOption.__members__:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid qualification option")
        if not qualification_img.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Require qualification image upload")

        stmt = select(VolunteerDoctor).where(VolunteerDoctor.email == email)
        existing_doctor_with_email = (await self.db.execute(stmt)).scalar_one_or_none()
        if existing_doctor_with_email is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

        dr_acc_creation_req = DoctorAccountCreationRequest(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password=password,
            qualification_option=DoctorQualificationOption[qualification_option],
            qualification_img_data=await qualification_img.read(),
        )
        self.db.add(dr_acc_creation_req)

    # async def get_account_creation_requests(self) -> list[AccountCreationRequestView]:
    #     doctor_creation_reqs = (await self.db.execute(select(DoctorAccountCreationRequest))).all()
    #     nutritionist_creation_reqs = (await self.db.execute(select(DoctorAccountCreationRequest))).all()
    #     return []

    # async def accept_account_creation_request(self, request_id: int) -> None:
    #     stmt = select(DoctorAccountCreationRequest).where(DoctorAccountCreationRequest.id == request_id)
    #     acc_creation_req = (await self.db.execute(stmt)).scalar_one_or_none()
    #     if acc_creation_req is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account creation request not found")

    # async def reject_account_creation_request(self, request_id: int) -> None:
    #     stmt = select(DoctorAccountCreationRequest).where(DoctorAccountCreationRequest.id == request_id)
    #     acc_creation_req = (await self.db.execute(stmt)).scalar_one_or_none()
    #     if acc_creation_req is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account creation request not found")
