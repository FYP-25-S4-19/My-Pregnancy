from app.core.exceptions import MetricCategoryNotFound
from sqlalchemy.orm import Session
from app.db.db_schema import (
    MedicalCredentialOption,
    BinaryMetricCategory,
    EduArticleCategory,
    BinaryMetric,
    ScalarMetric,
    Role,
)


class DefaultsGenerator:
    @staticmethod
    def generate_defaults(
        db: Session,
    ) -> tuple[list[MedicalCredentialOption], list[EduArticleCategory], list[BinaryMetric]]:
        DefaultsGenerator.init_roles(db)
        med_cred_options: list[MedicalCredentialOption] = DefaultsGenerator.init_med_cred_options(db)
        edu_article_categories: list[EduArticleCategory] = DefaultsGenerator.init_edu_article_categories(db)
        DefaultsGenerator.init_binary_metric_categories(db)
        all_metric_options: list[BinaryMetric] = DefaultsGenerator.init_binary_metrics(db)

        return (
            med_cred_options,
            edu_article_categories,
            all_metric_options,
        )

    @staticmethod
    def init_roles(db: Session) -> None:
        print("Initializing roles....")
        for role_label in [
            "PregnantWoman",
            "VolunteerSpecialist",
            "Admin",
            "Nutritionist",
        ]:
            role = Role(label=role_label)
            db.add(role)
        db.commit()

    @staticmethod
    def init_med_cred_options(db: Session) -> list[MedicalCredentialOption]:
        print("Initializing medical credential options....")

        med_cred_options: list[MedicalCredentialOption] = []
        for cred_label in [
            "Doctor of Medicine (M.D)",
            "Doctor of Osteopathic Medicine (D.O)",
            "Obstetrician/Gynecologist (OB/GYN)",
        ]:
            cred_option = MedicalCredentialOption(label=cred_label)
            med_cred_options.append(cred_option)
            db.add(cred_option)
        db.commit()
        return med_cred_options

    @staticmethod
    def init_edu_article_categories(db: Session) -> list[EduArticleCategory]:
        print("Initializing educational article categories.....")

        all_edu_article_categories: list[EduArticleCategory] = []
        for category_label in [
            "Nutrition",
            "Body",
            "Baby",
            "Feel good",
            "Medical",
            "Exercise",
            "Labour",
            "Lifestyle",
            "Relationships",
        ]:
            edu_article_category = EduArticleCategory(label=category_label)
            all_edu_article_categories.append(edu_article_category)
            db.add(edu_article_category)
        db.commit()
        return all_edu_article_categories

    @staticmethod
    def init_binary_metric_categories(db: Session) -> None:
        print("Initializing binary metric categories....")
        for category_label in [
            "Mood",
            "Symptoms",
            "Appetite",
            "Digestion",
            "Swelling",
            "Physical Activity",
            "Others",
        ]:
            metric_category = BinaryMetricCategory(label=category_label)
            db.add(metric_category)
        db.commit()

    # Each "Metric Option" has a "Metric Category"
    # Hence, why we seed this AFTER the categories are seeded
    @staticmethod
    def init_binary_metrics(db: Session) -> list[BinaryMetric]:
        mood_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Mood").first()
        )
        if mood_category is None:
            raise MetricCategoryNotFound("Mood")

        symptom_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Symptoms").first()
        )
        if symptom_category is None:
            raise MetricCategoryNotFound("Symptoms")

        appetite_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Appetite").first()
        )
        if appetite_category is None:
            raise MetricCategoryNotFound("Appetite")

        digestion_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Digestion").first()
        )
        if digestion_category is None:
            raise MetricCategoryNotFound("Digestion")

        swelling_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Swelling").first()
        )
        if swelling_category is None:
            raise MetricCategoryNotFound("Swelling")

        physical_activity_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Physical Activity").first()
        )
        if physical_activity_category is None:
            raise MetricCategoryNotFound("Physical Activity")

        others_category: BinaryMetricCategory | None = (
            db.query(BinaryMetricCategory).filter(BinaryMetricCategory.label == "Others").first()
        )
        if others_category is None:
            raise MetricCategoryNotFound("Others")

        all_metric_options: list[BinaryMetric] = [
            BinaryMetric(label="Calm", category=mood_category),
            BinaryMetric(label="Happy", category=mood_category),
            BinaryMetric(label="Energetic", category=mood_category),
            BinaryMetric(label="Mood Swings", category=mood_category),
            BinaryMetric(label="Irritated", category=mood_category),
            BinaryMetric(label="Sad", category=mood_category),
            BinaryMetric(label="Anxious", category=mood_category),
            BinaryMetric(label="Depressed", category=mood_category),
            BinaryMetric(label="Guilty", category=mood_category),
            BinaryMetric(label="Low Energy", category=mood_category),
            BinaryMetric(label="Apathetic", category=mood_category),
            BinaryMetric(label="Confused", category=mood_category),
            BinaryMetric(label="Self-critical", category=mood_category),
            BinaryMetric(label="Cramps", category=symptom_category),
            BinaryMetric(label="Headache", category=symptom_category),
            BinaryMetric(label="Acne", category=symptom_category),
            BinaryMetric(label="Backache", category=symptom_category),
            BinaryMetric(label="Fatigue", category=symptom_category),
            BinaryMetric(label="Cravings", category=symptom_category),
            BinaryMetric(label="Insomnia", category=symptom_category),
            BinaryMetric(label="Abdominal pain", category=symptom_category),
            BinaryMetric(label="Bleeding Gums", category=symptom_category),
            BinaryMetric(label="Food aversions", category=appetite_category),
            BinaryMetric(label="Increased appetite", category=appetite_category),
            BinaryMetric(label="Decreased appetite", category=appetite_category),
            BinaryMetric(label="Limbs swelling", category=swelling_category),
            BinaryMetric(label="Face swelling", category=swelling_category),
            BinaryMetric(label="Nasal congestion", category=swelling_category),
            BinaryMetric(label="Yoga", category=physical_activity_category),
            BinaryMetric(label="Gym", category=physical_activity_category),
            BinaryMetric(label="Swimming", category=physical_activity_category),
            BinaryMetric(label="Aerobics", category=physical_activity_category),
            BinaryMetric(label="Dancing", category=physical_activity_category),
            BinaryMetric(label="Running", category=physical_activity_category),
            BinaryMetric(label="Walking", category=physical_activity_category),
            BinaryMetric(label="Cycling", category=physical_activity_category),
            BinaryMetric(label="Team sports", category=physical_activity_category),
            BinaryMetric(label="Travel", category=others_category),
            BinaryMetric(label="Stress", category=others_category),
            BinaryMetric(label="Disease", category=others_category),
            BinaryMetric(label="Injury", category=others_category),
            BinaryMetric(label="Alcohol", category=others_category),
        ]
        print("Initializing binary metrics....")
        for metric_option in all_metric_options:
            db.add(metric_option)

        db.commit()
        return all_metric_options

    # TODO
    @staticmethod
    def init_scalar_metrics(db: Session) -> list[ScalarMetric]:
        print("Initializing scalar metrics....")

        metrics: list[ScalarMetric] = [
            ScalarMetric(label="Blood Pressure", unit_of_measurement=""),
            ScalarMetric(label="Sugar Level", unit_of_measurement="mmol/L"),
            ScalarMetric(label="Heart Rate", unit_of_measurement="bpm"),
            ScalarMetric(label="Weight", unit_of_measurement="kg"),
        ]
        for metric in metrics:
            db.add(metric)
        db.commit()
        return metrics
