from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session, selectinload

from app.db.db_schema import BinaryMetric, JournalEntry, JournalScalarMetricLog
from app.features.journal.journal_models import (
    BinaryMetricCategoryGroup,
    BinaryMetricView,
    BloodPressureView,
    JournalEntryResponse,
    ScalarMetricView,
)


class JournalService:
    def __init__(self, db: Session):
        self.db = db

    def get_journal_entries_for_mother(self, mother_id: int) -> list[JournalEntryResponse]:
        # Fetch all possible options
        #
        # We need this to render the "unselected" options (False).
        # We sort by ID so the UI always renders them in the same order.
        all_binary_defs: Sequence[BinaryMetric] = self.db.scalars(select(BinaryMetric).order_by(BinaryMetric.id)).all()

        # Fetch user data
        stmt = (
            select(JournalEntry)
            .where(JournalEntry.author_id == mother_id)
            .options(
                # Load SELECTED Binary Logs
                selectinload(JournalEntry.journal_binary_metric_logs),
                # Load Scalar Logs AND their Definitions (Label/Units)
                selectinload(JournalEntry.journal_scalar_metric_logs).joinedload(JournalScalarMetricLog.scalar_metric),
            )
            .order_by(JournalEntry.logged_on.desc())
        )
        entries = self.db.scalars(stmt).all()

        response_list: list[JournalEntryResponse] = []
        for entry in entries:
            selected_ids: set[int] = {log.binary_metric_id for log in entry.journal_binary_metric_logs}

            grouped_binary: defaultdict[str, list[BinaryMetricView]] = defaultdict(list)
            for definition in all_binary_defs:
                is_selected: bool = definition.id in selected_ids
                view_model = BinaryMetricView(
                    metric_id=definition.id,  # ID for future edits
                    label=definition.label,  # Text for display
                    category=definition.category.value,
                    is_selected=is_selected,
                )
                grouped_binary[definition.category.value].append(view_model)

            binary_metrics_response: list[BinaryMetricCategoryGroup] = [  # Convert to list
                BinaryMetricCategoryGroup(category=cat, binary_metric_logs=logs) for cat, logs in grouped_binary.items()
            ]

            scalar_metrics_response = []
            for log in entry.journal_scalar_metric_logs:
                scalar_metrics_response.append(
                    ScalarMetricView(
                        metric_id=log.scalar_metric.id,  # ID for future edits
                        label=log.scalar_metric.label,
                        value=log.value,
                        unit_of_measurement=log.scalar_metric.unit_of_measurement,
                    )
                )

            response_list.append(
                JournalEntryResponse(
                    id=entry.id,
                    logged_on=entry.logged_on,
                    content=entry.content,
                    binary_metrics=binary_metrics_response,
                    scalar_metrics=scalar_metrics_response,
                    blood_pressure=BloodPressureView(systolic=entry.systolic, diastolic=entry.diastolic),
                )
            )
        return response_list

    # def create_journal_entry(self, mother_id: int, request: JournalEntryCreateRequest) -> None:
    #     pass
    #
    # def edit_journal_entry(self, entry_id: int, mother_id: int, request: JournalEntryEditRequest) -> None:
    #     pass
    #     # 1. Fetch the entry with its relationships loaded
    #     # (Crucial so we can modify the collections)
    #     stmt = (
    #         select(JournalEntry)
    #         .where(JournalEntry.id == entry_id)
    #         .options(
    #             selectinload(JournalEntry.journal_binary_metric_logs),
    #             selectinload(JournalEntry.journal_scalar_metric_logs),
    #         )
    #     )
    #     journal_entry = self.db.scalars(stmt).first()
    #
    #     if journal_entry is None:
    #         raise HTTPException(status_code=404, detail="Journal entry not found")
    #     if journal_entry.author_id != mother_id:
    #         raise HTTPException(status_code=403, detail="Not authorized")
    #
    #     # 2. Update Simple Fields
    #     if request.content is not None:
    #         journal_entry.content = request.content
    #
    #     if request.blood_pressure is not None:
    #         journal_entry.systolic = request.blood_pressure.systolic
    #         journal_entry.diastolic = request.blood_pressure.diastolic
    #
    #     # ---------------------------------------------------------
    #     # PRE-FETCH LOOKUPS (Performance Optimization)
    #     # We need to convert labels ("Happy", "Weight") -> IDs (1, 5)
    #     # ---------------------------------------------------------
    #     if request.binary_metrics is not None or request.scalar_metrics is not None:
    #         # Fetch all possible metric definitions to map Label -> ID
    #         all_binary_metrics = self.db.scalars(select(BinaryMetric)).all()
    #         binary_map = {m.label: m.id for m in all_binary_metrics}
    #
    #         all_scalar_metrics = self.db.scalars(select(ScalarMetric)).all()
    #         scalar_map = {m.label: m.id for m in all_scalar_metrics}
    #
    #     # ---------------------------------------------------------
    #     # 3. Update Scalar Metrics
    #     # ---------------------------------------------------------
    #     if request.scalar_metrics is not None:
    #         # Strategy: Clear the existing list and rebuild it.
    #         # SQLAlchemy will issue DELETEs for removed items and INSERTs for new ones.
    #         journal_entry.journal_scalar_metric_logs.clear()
    #
    #         for sm_req in request.scalar_metrics:
    #             if sm_req.label in scalar_map:
    #                 new_log = JournalScalarMetricLog(scalar_metric_id=scalar_map[sm_req.label], value=sm_req.value)
    #                 journal_entry.journal_scalar_metric_logs.append(new_log)
    #
    #     # ---------------------------------------------------------
    #     # 4. Update Binary Metrics
    #     # ---------------------------------------------------------
    #     if request.binary_metrics is not None:
    #         journal_entry.journal_binary_metric_logs.clear()
    #
    #         # The request comes in grouped by category, but we just need the inner logs
    #         for category_group in request.binary_metrics:
    #             for bm_req in category_group.binary_metric_logs:
    #                 # Only add if it is selected AND exists in our DB map
    #                 if bm_req.is_selected and bm_req.label in binary_map:
    #                     new_log = JournalBinaryMetricLog(binary_metric_id=binary_map[bm_req.label])
    #                     journal_entry.journal_binary_metric_logs.append(new_log)

    def delete_journal_entry(self, entry_id: int, mother_id: int) -> None:
        journal_entry = self.db.get(JournalEntry, entry_id)
        if journal_entry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
        if journal_entry.author_id != mother_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this entry")
        self.db.delete(journal_entry)
