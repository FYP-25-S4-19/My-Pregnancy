from dataclasses import dataclass
from datetime import date

from app.core.custom_base_model import CustomBaseModel


@dataclass
class BinaryMetricView:
    metric_id: int
    label: str
    category: str
    is_selected: bool


@dataclass
class BinaryMetricCategoryGroup:
    category: str
    binary_metric_logs: list[BinaryMetricView]


@dataclass
class ScalarMetricView:
    metric_id: int
    label: str
    value: float
    unit_of_measurement: str


@dataclass
class BloodPressureView:
    systolic: int
    diastolic: int


class JournalEntryResponse(CustomBaseModel):
    id: int
    logged_on: date
    content: str
    binary_metrics: list[BinaryMetricCategoryGroup]
    scalar_metrics: list[ScalarMetricView]
    blood_pressure: BloodPressureView


# class JournalEntryCreateRequest(CustomBaseModel):
#     logged_on: date
#     content: str | None = None
#     binary_metrics: list[BinaryMetricLogsForCategory] | None = None
#     scalar_metrics: list[ScalarMetricLog] | None = None
#     blood_pressure: BloodPressure | None = None
#
#
# class JournalEntryEditRequest(CustomBaseModel):
#     content: str | None = None
#     binary_metrics: list[BinaryMetricLogsForCategory] | None = None
#     scalar_metrics: list[ScalarMetricLog] | None = None
#     blood_pressure: BloodPressure | None = None
