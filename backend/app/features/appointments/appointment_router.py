from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import PregnantWoman, User, VolunteerDoctor
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


@appointments_router.post("/")
def create_appointment(
    req: CreateAppointmentRequest,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    mother: PregnantWoman = require_role(PregnantWoman),
):
    try:
        service.create_appointment_request(req.doctor_id, mother.id, req.start_time)
        db.commit()
    except:
        db.rollback()
        raise


@appointments_router.get("/", response_model=list[AppointmentResponse])
def get_all_appointments_for_doctor(
    service: AppointmentService = Depends(get_appointment_service),
    user: User = require_role(User),
) -> list[AppointmentResponse]:
    return service.get_all_appointments_for_doctor(user.id)


@appointments_router.patch("/")
def edit_appointment_details(
    req: EditAppointmentRequest,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    mother: PregnantWoman = require_role(PregnantWoman),
):
    try:
        service.edit_appointment_details(req, mother.id)
        db.commit()
    except:
        db.rollback()
        raise


@appointments_router.delete("/")
def delete_appointment(
    req: DeleteAppointmentRequest,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    mother: PregnantWoman = require_role(PregnantWoman),
):
    try:
        service.delete_appointment(req, mother.id)
        db.commit()
    except:
        db.rollback()
        raise
