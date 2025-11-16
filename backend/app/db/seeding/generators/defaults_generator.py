from sqlalchemy.orm import Session

from app.db.db_schema import (
    BinaryMetric,
    BinaryMetricCategory,
    ScalarMetric,
)


class DefaultsGenerator:
    @staticmethod
    def generate_defaults(db: Session) -> tuple[list[BinaryMetric], list[ScalarMetric]]:
        binary_metrics = DefaultsGenerator.init_binary_metrics(db)
        scalar_metrics = DefaultsGenerator.init_scalar_metrics(db)
        return binary_metrics, scalar_metrics

    # Each "Metric Option" has a "Metric Category"
    # Hence, why we seed this AFTER the categories are seeded
    @staticmethod
    def init_binary_metrics(db: Session) -> list[BinaryMetric]:
        all_metric_options: list[BinaryMetric] = [
            BinaryMetric(label="Calm", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Happy", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Energetic", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Sad", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Anxious", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Low Energy", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Depressed", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Confused", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Irritated", category=BinaryMetricCategory.MOOD),
            # ======================================================================
            BinaryMetric(label="Everything is fine", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Cramps", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Tender breasts", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Headache", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Cravings", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Insomnia", category=BinaryMetricCategory.SYMPTOMS),
        ]
        print("Initializing binary metrics....")
        db.add_all(all_metric_options)
        db.commit()
        return all_metric_options

    @staticmethod
    def init_scalar_metrics(db: Session) -> list[ScalarMetric]:
        print("Initializing scalar metrics....")

        scalar_metrics: list[ScalarMetric] = [
            ScalarMetric(label="Water", unit_of_measurement="Litres"),
            ScalarMetric(label="Sugar Level", unit_of_measurement="mmol/L"),
            ScalarMetric(label="Heart Rate", unit_of_measurement="BPM"),
            ScalarMetric(label="Weight", unit_of_measurement="KG"),
        ]
        db.add_all(scalar_metrics)
        db.commit()
        return scalar_metrics
