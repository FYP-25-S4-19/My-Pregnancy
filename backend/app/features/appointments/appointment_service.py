from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.db_schema import Appointment, AppointmentStatus, PregnantWoman, User, UserRole, VolunteerDoctor
from app.features.appointments.appointment_models import (
    AppointmentResponse,
    EditAppointmentRequest,
)


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment_request(self, doctor_id: int, requester_id: int, start_time: datetime) -> None:
        doctor = self.db.get(VolunteerDoctor, doctor_id)
        if doctor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified doctor does not exist")

        appointment = Appointment(
            doctor_id=doctor_id,
            mother_id=requester_id,
            start_time=start_time,
            status=AppointmentStatus.PENDING_ACCEPT_REJECT,
        )
        self.db.add(appointment)

    def get_all_appointments(self, user: User) -> list[AppointmentResponse]:
        is_participant: bool = user.role == UserRole.PREGNANT_WOMAN or user.role == UserRole.VOLUNTEER_DOCTOR
        if not is_participant:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        all_appointments = (
            self.db.query(Appointment).where(Appointment.volunteer_doctor_id == user.id).all()
            if user.role == UserRole.VOLUNTEER_DOCTOR
            else self.db.query(Appointment).where(Appointment.mother_id == user.id).all()
        )

        response: list[AppointmentResponse] = []
        for appointment in all_appointments:
            doctor: VolunteerDoctor = appointment.volunteer_doctor
            mother: PregnantWoman = appointment.mother

            response.append(
                AppointmentResponse(
                    doctor_id=doctor.id,
                    doctor_name=(
                        f"{doctor.first_name} {doctor.middle_name if doctor.middle_name is not None else ''} {doctor.last_name}"
                    ),
                    mother_id=mother.id,
                    mother_username=mother.username,
                    start_time=appointment.start_time,
                    status=appointment.status.value,
                )
            )
        return response

    def edit_appointment_details(self, req: EditAppointmentRequest, mother_id: int) -> None:
        appointment = self.db.get(Appointment, req.appointment_id)
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid appointment ID")
        if appointment.mother_id != mother_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Attempting to modify appointment for another entity"
            )
        appointment.start_time = req.start_time

    def delete_appointment(self, appointment_id: int, mother_id: int) -> None:
        appointment = self.db.get(Appointment, appointment_id)
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if appointment.mother_id != mother_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        self.db.delete(appointment)
