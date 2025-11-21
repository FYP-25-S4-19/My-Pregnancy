from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import PregnantWoman, User
from app.features.appointments.appointment_models import (
    AppointmentResponse,
    CreateAppointmentRequest,
    DeleteAppointmentRequest,
    EditAppointmentRequest,
)
from app.features.appointments.appointment_service import AppointmentService

appointments_router = APIRouter(prefix="/appointments")


def get_appointment_service(db: Session = Depends(get_db)) -> AppointmentService:
    return AppointmentService(db)


@appointments_router.post("/", status_code=status.HTTP_201_CREATED)
def create_appointment(
    request: CreateAppointmentRequest,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
):
    try:
        service.create_appointment_request(request.doctor_id, mother.id, request.start_time)
        db.commit()
    except:
        db.rollback()
        raise


@appointments_router.get("/", response_model=list[AppointmentResponse])
def get_all_appointments(
    service: AppointmentService = Depends(get_appointment_service), user: User = Depends(require_role(User))
) -> list[AppointmentResponse]:
    return service.get_all_appointments(user)


@appointments_router.patch("/")
def edit_appointment_start_time(
    request: EditAppointmentRequest,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
):
    try:
        service.edit_appointment_start_time(request, mother.id)
        db.commit()
    except:
        db.rollback()
        raise


@appointments_router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
):
    try:
        service.delete_appointment(appointment_id, mother.id)
        db.commit()
    except:
        db.rollback()
        raise
