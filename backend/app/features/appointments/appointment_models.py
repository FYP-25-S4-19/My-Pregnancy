from datetime import datetime

from app.core.custom_base_model import CustomBaseModel


class CreateAppointmentRequest(CustomBaseModel):
    doctor_id: int
    start_time: datetime


class AppointmentResponse(CustomBaseModel):
    doctor_id: int
    doctor_name: str

    mother_id: int
    mother_username: str

    start_time: datetime
    status: str


class EditAppointmentRequest(CustomBaseModel):
    appointment_id: int
    start_time: datetime


class DeleteAppointmentRequest(CustomBaseModel):
    appointment_id: int
