from sqlalchemy.orm import Session
from datetime import datetime
from app.db_schema import (
    PregnantWoman,
    MetricOption,
    JournalEntry,
    MetricLog,
    User,
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
    def generate_metric_logs(
        db: Session,
        journal_entries: list[JournalEntry],
        metric_options: list[MetricOption],
    ):
        print("Generating Metric Logs....")
        for journal_entry in journal_entries:
            num_selected_options = random.randint(0, len(metric_options))
            selected_metric_options = random.sample(population=metric_options, k=num_selected_options)
            for metric_option in selected_metric_options:
                metric_log = MetricLog(journal_entry=journal_entry, metric_option=metric_option)
                db.add(metric_log)
        db.commit()
