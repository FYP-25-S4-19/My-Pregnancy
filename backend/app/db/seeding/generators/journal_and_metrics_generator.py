from sqlalchemy.orm import Session
from datetime import datetime
from app.db.db_schema import (
    PregnantWoman,
    BinaryMetric,
    JournalEntry,
    JournalBinaryMetricLog,
    User,
    ScalarMetric,
)
from faker import Faker
import random


class JournalAndMetricsGenerator:
    @staticmethod
    def generate_journal_entries(
        db: Session, faker: Faker, all_preg_women: list[PregnantWoman], count: int
    ) -> list[JournalEntry]:
        print("Generating journal entries.....")

        entries: list[JournalEntry] = []
        for _ in range(count):
            user: User = random.choice(all_preg_women)
            journal_entry = JournalEntry(
                author=user,
                content=faker.paragraph(nb_sentences=random.randint(2, 10)),
                logged_at=faker.date_time_between(start_date=user.created_at, end_date=datetime.now()),
            )
            db.add(journal_entry)
        db.commit()
        return entries

    @staticmethod
    def generate_journal_binary_metric_logs(
        db: Session,
        journal_entries: list[JournalEntry],
        binary_metrics: list[BinaryMetric],
    ):
        print("Generating journal 'binary metric' logs....")
        for journal_entry in journal_entries:
            num_selected_options = random.randint(0, len(binary_metrics))
            selected_metric_options = random.sample(population=binary_metrics, k=num_selected_options)
            for metric_option in selected_metric_options:
                metric_log = JournalBinaryMetricLog(journal_entry=journal_entry, metric_option=metric_option)
                db.add(metric_log)
        db.commit()

    # TODO
    # @staticmethod
    # def generate_journal_scalar_metric_logs(
    #     db: Session,
    #     journal_entries: list[JournalEntry],
    #     scalar_metrics: list[ScalarMetric],
    # ):
    #     print("Generating journal 'scalar metric' logs....")
    #     for journal_entry in journal_entries:
    #         num_selected_metrics = random.randint(0, len(scalar_metrics))
    #         selected_scalar_metrics = random.sample(population=scalar_metrics, k=num_selected_metrics)
    #         for metric_option in selected_scalar_metrics:
    #             metric_log = JournalBinaryMetricLog(journal_entry=journal_entry, metric_option=metric_option)
    #             db.add(metric_log)
    #     db.commit()
