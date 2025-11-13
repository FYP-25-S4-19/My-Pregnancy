from sqlalchemy.orm import Session
from app.db.db_schema import (
    BinaryMetricCategory,
    BinaryMetric,
    ScalarMetric,
)


class DefaultsGenerator:
    @staticmethod
    def generate_defaults(db: Session) -> None:
        DefaultsGenerator.init_binary_metrics(db)

    # Each "Metric Option" has a "Metric Category"
    # Hence, why we seed this AFTER the categories are seeded
    @staticmethod
    def init_binary_metrics(db: Session) -> list[BinaryMetric]:
        all_metric_options: list[BinaryMetric] = [
            BinaryMetric(label="Calm", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Happy", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Energetic", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Mood Swings", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Irritated", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Sad", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Anxious", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Depressed", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Guilty", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Low Energy", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Apathetic", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Confused", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Self-critical", category=BinaryMetricCategory.MOOD),
            BinaryMetric(label="Cramps", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Headache", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Acne", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Backache", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Fatigue", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Cravings", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Insomnia", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Abdominal pain", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Bleeding Gums", category=BinaryMetricCategory.SYMPTOMS),
            BinaryMetric(label="Food aversions", category=BinaryMetricCategory.APPETITE),
            BinaryMetric(label="Increased appetite", category=BinaryMetricCategory.APPETITE),
            BinaryMetric(label="Decreased appetite", category=BinaryMetricCategory.APPETITE),
            BinaryMetric(label="Limbs swelling", category=BinaryMetricCategory.SWELLING),
            BinaryMetric(label="Face swelling", category=BinaryMetricCategory.SWELLING),
            BinaryMetric(label="Nasal congestion", category=BinaryMetricCategory.SWELLING),
            BinaryMetric(label="Yoga", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Gym", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Swimming", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Aerobics", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Dancing", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Running", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Walking", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Cycling", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Team sports", category=BinaryMetricCategory.PHYSICAL_ACTIVITY),
            BinaryMetric(label="Travel", category=BinaryMetricCategory.OTHERS),
            BinaryMetric(label="Stress", category=BinaryMetricCategory.OTHERS),
            BinaryMetric(label="Disease", category=BinaryMetricCategory.OTHERS),
            BinaryMetric(label="Injury", category=BinaryMetricCategory.OTHERS),
            BinaryMetric(label="Alcohol", category=BinaryMetricCategory.OTHERS),
        ]
        print("Initializing binary metrics....")
        for metric_option in all_metric_options:
            db.add(metric_option)

        db.commit()
        return all_metric_options

    # # TODO
    # @staticmethod
    # def init_scalar_metrics(db: Session) -> list[ScalarMetric]:
    #     print("Initializing scalar metrics....")
    #
    #     metrics: list[ScalarMetric] = [
    #         ScalarMetric(label="Blood Pressure", unit_of_measurement=""),
    #         ScalarMetric(label="Sugar Level", unit_of_measurement="mmol/L"),
    #         ScalarMetric(label="Heart Rate", unit_of_measurement="bpm"),
    #         ScalarMetric(label="Weight", unit_of_measurement="kg"),
    #     ]
    #     for metric in metrics:
    #         db.add(metric)
    #     db.commit()
    #     return metrics
