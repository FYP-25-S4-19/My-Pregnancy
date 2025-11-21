import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from app.db.db_schema import (
    BinaryMetric,
    JournalBinaryMetricLog,
    JournalEntry,
    JournalScalarMetricLog,
    PregnantWoman,
    ScalarMetric,
)


class JournalAndMetricsGenerator:
    @staticmethod
    def generate_journal_entries(
        db: Session, faker: Faker, all_preg_women: list[PregnantWoman], max_entries_per_author: int
    ) -> list[JournalEntry]:
        print("Generating journal entries.....")

        journal_entries: list[JournalEntry] = []
        for preg_woman in all_preg_women:
            rand_entry_count = random.randrange(0, max_entries_per_author)
            for day_offset in range(rand_entry_count):
                journal_entry = JournalEntry(
                    author=preg_woman,
                    content=(
                        faker.paragraph(nb_sentences=random.randint(1, 7))
                        if random.random() > 0.75
                        else ""  # 75% chance of there being a written entry
                    ),
                    logged_on=date.today() - timedelta(days=day_offset),
                )
                journal_entries.append(journal_entry)
                db.add(journal_entry)
        db.commit()
        return journal_entries

    @staticmethod
    def generate_journal_metric_logs(
        db: Session,
        journal_entries: list[JournalEntry],
        binary_metrics: list[BinaryMetric],
        scalar_metrics: list[ScalarMetric],
    ) -> None:
        print("Generating journal 'metric (scalar and binary)' logs....")
        for journal_entry in journal_entries:
            # ---- Binary Metrics ----
            num_binary_metrics: int = random.randint(0, len(binary_metrics))
            selected_binary_metrics: list[BinaryMetric] = random.sample(population=binary_metrics, k=num_binary_metrics)
            for binary_metric in selected_binary_metrics:
                metric_log = JournalBinaryMetricLog(journal_entry=journal_entry, binary_metric=binary_metric)
                db.add(metric_log)

            # ---- Scalar Metrics ----
            scalar_metric_logs: list[JournalScalarMetricLog] = []
            num_scalar_metrics: int = random.randint(0, len(scalar_metrics))
            selected_scalar_metrics: list[ScalarMetric] = random.sample(population=scalar_metrics, k=num_scalar_metrics)
            for scalar_metric in selected_scalar_metrics:
                val: float = 0
                if scalar_metric.label == "Water":
                    val = random.uniform(1, 2.5)
                elif scalar_metric.label == "Sugar Level":
                    val = random.uniform(70, 110)
                elif scalar_metric.label == "Heart Rate":
                    val = random.uniform(50, 105)
                elif scalar_metric.label == "Weight":
                    val = random.uniform(50, 85)
                else:
                    print("ERROR - Found a metric label with an invalid label: ", scalar_metric.label)
                metric_log = JournalScalarMetricLog(journal_entry=journal_entry, scalar_metric=scalar_metric, value=val)
                scalar_metric_logs.append(metric_log)
                db.add(metric_log)

            # ----- Blood Pressure ----
            if random.random() <= 0.1:  # 10% chance of there NOT being an entry
                continue
            journal_entry.systolic = random.randint(90, 140)
            journal_entry.diastolic = random.randint(60, 90)

        db.commit()
