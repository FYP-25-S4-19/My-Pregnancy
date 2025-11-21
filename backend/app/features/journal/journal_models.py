from dataclasses import dataclass
from datetime import date

from app.core.custom_base_model import CustomBaseModel


class BinaryMetricLog(CustomBaseModel):
    label: str
    is_selected: bool


@dataclass
class BinaryMetricLogsForCategory:
    category: str
    binary_metric_logs: list[BinaryMetricLog]


@dataclass
class ScalarMetricLog:
    label: str
    value: float
    unit_of_measurement: str


@dataclass
class BloodPressure:
    systolic: int
    diastolic: int


class JournalEntryLogsResponse(CustomBaseModel):
    id: int
    logged_on: date
    content: str
    binary_metrics: list[BinaryMetricLogsForCategory]
    scalar_metric: list[ScalarMetricLog]
    blood_pressure: BloodPressure
