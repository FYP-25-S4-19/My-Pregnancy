from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.db_schema import Appointment, AppointmentStatus, PregnantWoman, User, UserRole, VolunteerDoctor
from app.features.appointments.appointment_models import (
    AppointmentResponse,
    EditAppointmentRequest,
)


class AppointmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_appointment_request(self, doctor_id: int, requester_id: int, start_time: datetime) -> None:
        doctor = await self.db.get(VolunteerDoctor, doctor_id)
        if doctor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified doctor does not exist")

        if start_time <= datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start time must be in the future")

        appointment = Appointment(
            volunteer_doctor_id=doctor_id,
            mother_id=requester_id,
            start_time=start_time,
            status=AppointmentStatus.PENDING_ACCEPT_REJECT,
        )
        self.db.add(appointment)

    async def get_all_appointments(self, user: User) -> list[AppointmentResponse]:
        is_participant: bool = user.role == UserRole.PREGNANT_WOMAN or user.role == UserRole.VOLUNTEER_DOCTOR
        if not is_participant:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        query = select(Appointment).options(
            selectinload(Appointment.volunteer_doctor), selectinload(Appointment.mother)
        )

        if user.role == UserRole.VOLUNTEER_DOCTOR:
            query = query.where(Appointment.volunteer_doctor_id == user.id)
        else:
            query = query.where(Appointment.mother_id == user.id)

        result = await self.db.execute(query)
        all_appointments = result.scalars().all()

        response: list[AppointmentResponse] = []
        for appointment in all_appointments:
            doctor: VolunteerDoctor = appointment.volunteer_doctor
            mother: PregnantWoman = appointment.mother

            response.append(
                AppointmentResponse(
                    appointment_id=appointment.id,
                    doctor_id=doctor.id,
                    doctor_name=" ".join(
                        part for part in [doctor.first_name, doctor.middle_name, doctor.last_name] if part
                    ),
                    mother_id=mother.id,
                    mother_username=mother.username,
                    start_time=appointment.start_time,
                    status=appointment.status.value,
                )
            )
        return response

    async def edit_appointment_start_time(self, req: EditAppointmentRequest, mother_id: int) -> None:
        appointment = await self.db.get(Appointment, req.appointment_id)
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid appointment ID")
        if appointment.mother_id != mother_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Attempting to modify appointment for another entity"
            )
        if req.new_start_time <= datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start time must be in the future")

        appointment.start_time = req.new_start_time

    async def delete_appointment(self, appointment_id: int, mother_id: int) -> None:
        appointment = await self.db.get(Appointment, appointment_id)
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if appointment.mother_id != mother_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        await self.db.delete(appointment)

    async def accept_appointment(self, appointment_id: int, doctor_id: int) -> None:
        appointment = await self.db.get(Appointment, appointment_id)
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if appointment.volunteer_doctor_id != doctor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        if appointment.status == AppointmentStatus.ACCEPTED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Appointment is already accepted")
        if appointment.status != AppointmentStatus.PENDING_ACCEPT_REJECT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Only pending appointments can be accepted"
            )
        appointment.status = AppointmentStatus.ACCEPTED

    async def reject_appointment(self, appointment_id: int, doctor_id: int) -> None:
        appointment = await self.db.get(Appointment, appointment_id)
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if appointment.volunteer_doctor_id != doctor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        if appointment.status == AppointmentStatus.REJECTED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Appointment is already rejected")
        if appointment.status != AppointmentStatus.PENDING_ACCEPT_REJECT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Only pending appointments can be rejected"
            )
        appointment.status = AppointmentStatus.REJECTED
