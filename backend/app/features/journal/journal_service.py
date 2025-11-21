from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.db_schema import JournalBinaryMetricLog, JournalEntry, JournalScalarMetricLog
from app.features.journal.journal_models import (
    BinaryMetricLog,
    BinaryMetricLogsForCategory,
    BloodPressure,
    JournalEntryLogsResponse,
    ScalarMetricLog,
)


class JournalService:
    def __init__(self, db: Session):
        self.db = db

    def get_journal_entries_for_mother(self, mother_id: int) -> list[JournalEntryLogsResponse]:
        # 1. Build the Query
        # We use 'selectinload' for the One-To-Many collections (logs) to avoid Cartesian products
        # We use 'joinedload' for the Many-To-One (metric definitions) because it's a single join
        stmt = (
            select(JournalEntry)
            .where(JournalEntry.author_id == mother_id)
            .options(
                # Load Scalar Logs + The definition of the metric (label, unit)
                selectinload(JournalEntry.journal_scalar_metric_logs).joinedload(JournalScalarMetricLog.scalar_metric),
                # Load Binary Logs + The definition (label, category)
                selectinload(JournalEntry.journal_binary_metric_logs).joinedload(JournalBinaryMetricLog.binary_metric),
            )
            .order_by(JournalEntry.logged_on.desc())
        )

        entries = self.db.scalars(stmt).all()

        # 2. Transform ORM Objects to Pydantic/Dataclasses
        response_list = []

        for entry in entries:
            # --- Map Blood Pressure ---
            bp_data = BloodPressure(systolic=entry.systolic, diastolic=entry.diastolic)

            # --- Map Scalar Metrics ---
            scalar_logs = []
            for log in entry.journal_scalar_metric_logs:
                scalar_logs.append(
                    ScalarMetricLog(
                        label=log.scalar_metric.label,
                        value=log.value,
                        unit_of_measurement=log.scalar_metric.unit_of_measurement,
                    )
                )

            # --- Map & Group Binary Metrics ---
            # We must group the flat list of logs by their Category (Mood, Symptoms, etc.)
            # A temporary dictionary to hold lists: { "MOOD": [Log1, Log2], "SYMPTOMS": [Log3] }
            grouped_binary = defaultdict(list)

            for log in entry.journal_binary_metric_logs:
                category_name = log.binary_metric.category.value  # Get Enum string value

                metric_log_model = BinaryMetricLog(
                    label=log.binary_metric.label,
                    is_selected=True,  # Since the record exists in the DB, it is selected
                )
                grouped_binary[category_name].append(metric_log_model)

            # Convert the dict to the expected List[BinaryMetricLogsForCategory]
            binary_metrics_response = []
            for category, logs in grouped_binary.items():
                binary_metrics_response.append(BinaryMetricLogsForCategory(category=category, binary_metric_logs=logs))

            # --- Final Assembly ---
            response_list.append(
                JournalEntryLogsResponse(
                    id=entry.id,
                    logged_on=entry.logged_on,
                    content=entry.content,
                    binary_metrics=binary_metrics_response,
                    scalar_metric=scalar_logs,
                    blood_pressure=bp_data,
                )
            )

        return response_list
