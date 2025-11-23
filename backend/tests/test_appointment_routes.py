from datetime import datetime, timedelta
from typing import Callable

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.db_schema import (
    Appointment,
    AppointmentStatus,
    PregnantWoman,
    VolunteerDoctor,
)
from app.features.appointments.appointment_models import (
    CreateAppointmentRequest,
    EditAppointmentRequest,
)


# =========================================================================
# ========================= CREATE APPOINTMENT ============================
# =========================================================================
def test_create_appointment_success(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    volunteer_doctor: VolunteerDoctor,
    db_session: Session,
) -> None:
    client, mother = authenticated_pregnant_woman_client
    start_time: datetime = datetime.now() + timedelta(days=1)

    response = client.post(
        "/appointments",
        content=CreateAppointmentRequest(doctor_id=volunteer_doctor.id, start_time=start_time).model_dump_json(),
    )
    assert response.status_code == status.HTTP_201_CREATED

    appointment = db_session.query(Appointment).filter_by(mother_id=mother.id).one_or_none()
    assert appointment is not None, "Appointment was not created in the database"
    assert appointment.start_time == start_time, "Appointment start time does not match"
    assert appointment.volunteer_doctor_id == volunteer_doctor.id, "Appointment doctor ID does not match"
    assert appointment.status == AppointmentStatus.PENDING_ACCEPT_REJECT, (
        "Appointment status should be PENDING_ACCEPT_REJECT"
    )


def test_create_appointment_doctor_not_found(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
) -> None:
    client, _ = authenticated_pregnant_woman_client
    start_time: datetime = datetime.now() + timedelta(days=1)
    invalid_doctor_id: int = 9999
    response = client.post(
        "/appointments",
        content=CreateAppointmentRequest(doctor_id=invalid_doctor_id, start_time=start_time).model_dump_json(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Doctor with ID {invalid_doctor_id} should not exist"


def test_create_appointment_past_start_time(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    volunteer_doctor: VolunteerDoctor,
) -> None:
    client, _ = authenticated_pregnant_woman_client
    past_start_time: datetime = datetime.now() - timedelta(days=1)
    response = client.post(
        "/appointments",
        content=CreateAppointmentRequest(doctor_id=volunteer_doctor.id, start_time=past_start_time).model_dump_json(),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, "Should not allow creating appointments in the past"


# =========================================================================
# ========================= EDIT APPOINTMENT ==============================
# =========================================================================
def test_edit_appointment_success(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    volunteer_doctor: VolunteerDoctor,
    db_session: Session,
) -> None:
    client, mother = authenticated_pregnant_woman_client

    start_time: datetime = datetime.now() + timedelta(days=5)
    appointment = Appointment(
        volunteer_doctor_id=volunteer_doctor.id,
        mother_id=mother.id,
        start_time=start_time,
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(appointment)
    db_session.commit()

    new_start_time: datetime = datetime.now() + timedelta(days=10)
    response = client.patch(
        "/appointments",
        content=EditAppointmentRequest(appointment_id=appointment.id, new_start_time=new_start_time).model_dump_json(),
    )
    assert response.status_code == status.HTTP_200_OK, "Editing appointment 'new_start_time' should succeed"


def test_edit_appointment_not_found(authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman]) -> None:
    client, _ = authenticated_pregnant_woman_client

    new_start_time: datetime = datetime.now() + timedelta(days=10)
    edit_response = client.patch(
        "/appointments",
        content=EditAppointmentRequest(appointment_id=9999, new_start_time=new_start_time).model_dump_json(),
    )
    assert edit_response.status_code == status.HTTP_404_NOT_FOUND, (
        "Editing a non-existent appointment should return 404"
    )


def test_edit_appointment_past_start_time(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    volunteer_doctor: VolunteerDoctor,
    db_session: Session,
) -> None:
    client, mother = authenticated_pregnant_woman_client

    appointment = Appointment(
        volunteer_doctor_id=volunteer_doctor.id,
        mother_id=mother.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(appointment)
    db_session.commit()

    past_start_time: datetime = datetime.now() - timedelta(days=1)
    edit_response = client.patch(
        "/appointments",
        content=EditAppointmentRequest(appointment_id=appointment.id, new_start_time=past_start_time).model_dump_json(),
    )
    assert edit_response.status_code == status.HTTP_400_BAD_REQUEST, (
        "Should not allow editing appointment to a past start time"
    )


# =========================================================================
# ======================= DELETE APPOINTMENT ==============================
# =========================================================================
def test_delete_appointment_success(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    volunteer_doctor: VolunteerDoctor,
    db_session: Session,
) -> None:
    client, mother = authenticated_pregnant_woman_client

    appointment = Appointment(
        volunteer_doctor_id=volunteer_doctor.id,
        mother_id=mother.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(appointment)
    db_session.commit()

    delete_response = client.delete(f"/appointments/{appointment.id}")
    assert delete_response.status_code == status.HTTP_200_OK, "Deleting appointment should succeed"

    deleted_appointment = db_session.get(Appointment, appointment.id)
    assert deleted_appointment is None, "Appointment should be deleted from the database"


def test_delete_appointment_not_found(authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman]) -> None:
    client, _ = authenticated_pregnant_woman_client
    delete_response = client.delete("/appointments/9999")
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND, (
        "Deleting non-existent appointment should return 404"
    )


def test_delete_appointment_for_other_user(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    pregnant_woman_factory: Callable[..., PregnantWoman],
    volunteer_doctor: VolunteerDoctor,
    db_session: Session,
) -> None:
    authorized_client, _ = authenticated_pregnant_woman_client
    other_mother: PregnantWoman = pregnant_woman_factory()

    other_mother_appointment = Appointment(
        volunteer_doctor_id=volunteer_doctor.id,
        mother_id=other_mother.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(other_mother_appointment)
    db_session.commit()

    delete_response = authorized_client.delete(f"/appointments/{other_mother_appointment.id}")
    assert delete_response.status_code == status.HTTP_403_FORBIDDEN, (
        "Should not allow deleting appointment belonging to another user"
    )


# =========================================================================
# ===================== ACCEPT/REJECT APPOINTMENT =========================
# =========================================================================
def test_accept_appointment_success(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    pregnant_woman: PregnantWoman,
    db_session: Session,
) -> None:
    client, doctor = authenticated_doctor_client

    appointment = Appointment(
        volunteer_doctor_id=doctor.id,
        mother_id=pregnant_woman.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(appointment)
    db_session.commit()
    accept_response = client.patch(f"/appointments/{appointment.id}/accept")
    assert accept_response.status_code == status.HTTP_200_OK, "Accepting appointment should succeed"

    updated_appointment = db_session.get(Appointment, appointment.id)
    assert updated_appointment is not None, "Appointment should exist in the database"
    assert updated_appointment.status == AppointmentStatus.ACCEPTED, "Appointment status should be ACCEPTED"


def test_reject_appointment_success(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    pregnant_woman: PregnantWoman,
    db_session: Session,
) -> None:
    client, doctor = authenticated_doctor_client

    appointment = Appointment(
        volunteer_doctor_id=doctor.id,
        mother_id=pregnant_woman.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(appointment)
    db_session.commit()
    reject_response = client.patch(f"/appointments/{appointment.id}/reject")
    assert reject_response.status_code == status.HTTP_200_OK, "Rejecting appointment should succeed"

    updated_appointment = db_session.get(Appointment, appointment.id)
    assert updated_appointment is not None, "Appointment should exist in the database"
    assert updated_appointment.status == AppointmentStatus.REJECTED, "Appointment status should be REJECTED"


def test_accept_appointment_not_found(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
) -> None:
    client, _ = authenticated_doctor_client
    accept_response = client.patch("/appointments/9999/accept")
    assert accept_response.status_code == status.HTTP_404_NOT_FOUND, (
        "Accepting non-existent appointment should return 404"
    )


def test_reject_appointment_not_found(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
) -> None:
    client, _ = authenticated_doctor_client
    reject_response = client.patch("/appointments/9999/reject")
    assert reject_response.status_code == status.HTTP_404_NOT_FOUND, (
        "Rejecting non-existent appointment should return 404"
    )


def test_accept_appointment_unauthorized(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    volunteer_doctor_factory: Callable[..., VolunteerDoctor],
    pregnant_woman: PregnantWoman,
    db_session: Session,
) -> None:
    authorized_client, _ = authenticated_doctor_client
    other_doctor: VolunteerDoctor = volunteer_doctor_factory()

    other_doctor_appointment = Appointment(
        volunteer_doctor_id=other_doctor.id,
        mother_id=pregnant_woman.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(other_doctor_appointment)
    db_session.commit()

    accept_response = authorized_client.patch(f"/appointments/{other_doctor_appointment.id}/accept")
    assert accept_response.status_code == status.HTTP_403_FORBIDDEN, (
        "Should not allow accepting appointment belonging to another doctor"
    )


def test_accept_appointment_already_accepted(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    pregnant_woman: PregnantWoman,
    db_session: Session,
) -> None:
    client, doctor = authenticated_doctor_client

    appointment = Appointment(
        volunteer_doctor_id=doctor.id,
        mother_id=pregnant_woman.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.ACCEPTED,
    )
    db_session.add(appointment)
    db_session.commit()

    accept_response = client.patch(f"/appointments/{appointment.id}/accept")
    assert accept_response.status_code == status.HTTP_409_CONFLICT, (
        "Should not be able to accept an already accepted appointment"
    )


def test_reject_appointment_unauthorized(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    volunteer_doctor_factory: Callable[..., VolunteerDoctor],
    pregnant_woman: PregnantWoman,
    db_session: Session,
) -> None:
    authorized_client, _ = authenticated_doctor_client
    other_doctor: VolunteerDoctor = volunteer_doctor_factory()

    other_doctor_appointment = Appointment(
        volunteer_doctor_id=other_doctor.id,
        mother_id=pregnant_woman.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.PENDING_ACCEPT_REJECT,
    )
    db_session.add(other_doctor_appointment)
    db_session.commit()

    reject_response = authorized_client.patch(f"/appointments/{other_doctor_appointment.id}/reject")
    assert reject_response.status_code == status.HTTP_403_FORBIDDEN, (
        "Should not allow rejecting appointment belonging to another doctor"
    )


def test_reject_appointment_already_rejected(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    pregnant_woman: PregnantWoman,
    db_session: Session,
) -> None:
    client, doctor = authenticated_doctor_client

    appointment = Appointment(
        volunteer_doctor_id=doctor.id,
        mother_id=pregnant_woman.id,
        start_time=datetime.now() + timedelta(days=5),
        status=AppointmentStatus.REJECTED,
    )
    db_session.add(appointment)
    db_session.commit()

    reject_response = client.patch(f"/appointments/{appointment.id}/reject")
    assert reject_response.status_code == status.HTTP_409_CONFLICT, (
        "Should not be able to reject an already rejected appointment"
    )
