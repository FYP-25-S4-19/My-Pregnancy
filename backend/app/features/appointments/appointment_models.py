from datetime import datetime
from uuid import UUID

from app.core.custom_base_model import CustomBaseModel


class CreateAppointmentRequest(CustomBaseModel):
    doctor_id: int
    start_time: datetime


class AppointmentResponse(CustomBaseModel):
    appointment_id: UUID

    doctor_id: int
    doctor_name: str

    mother_id: int
    mother_name: str

    start_time: datetime
    status: str


class EditAppointmentRequest(CustomBaseModel):
    appointment_id: UUID
    new_start_time: datetime
