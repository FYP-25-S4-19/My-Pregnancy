from app.db_schema import MedicalCredentialOption, EduArticleCategory, MetricCategory, MetricOption, Role
from app.exceptions.general_exceptions import MetricCategoryNotFound
from sqlalchemy.orm import Session


class DefaultsGenerator:
    @staticmethod
    def init_roles(db: Session) -> None:
        print("Initializing roles....")
        for role_label in ["PregnantWoman", "VolunteerSpecialist", "Admin"]:
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
            "Licensed Midwife (LM)",
            "Obstetrician/Gynecologist (OB/GYN)",
            "Certified Nurse-Midwife (CNM)",
            "Registered Nurse (RN)",
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
    def init_metric_categories(db: Session) -> None:
        print("Initializing metric categories....")
        for category_label in ["Mood", "Symptoms", "Appetite", "Digestion", "Swelling", "Physical Activity", "Others"]:
            metric_category = MetricCategory(label=category_label)
            db.add(metric_category)
        db.commit()

    # Each "Metric Option" has a "Metric Category"
    # Hence, why we seed this AFTER the categories are seeded
    @staticmethod
    def init_metric_options(db: Session) -> list[MetricOption]:
        mood_category: MetricCategory | None = db.query(MetricCategory).filter(MetricCategory.label == "Mood").first()
        if mood_category is None:
            raise MetricCategoryNotFound("Mood")

        symptom_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Symptoms").first()
        )
        if symptom_category is None:
            raise MetricCategoryNotFound("Symptoms")

        appetite_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Appetite").first()
        )
        if appetite_category is None:
            raise MetricCategoryNotFound("Appetite")

        digestion_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Digestion").first()
        )
        if digestion_category is None:
            raise MetricCategoryNotFound("Digestion")

        swelling_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Swelling").first()
        )
        if swelling_category is None:
            raise MetricCategoryNotFound("Swelling")

        physical_activity_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Physical Activity").first()
        )
        if physical_activity_category is None:
            raise MetricCategoryNotFound("Physical Activity")

        others_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Others").first()
        )
        if others_category is None:
            raise MetricCategoryNotFound("Others")

        all_metric_options: list[MetricOption] = [
            MetricOption(label="Calm", category=mood_category),
            MetricOption(label="Happy", category=mood_category),
            MetricOption(label="Energetic", category=mood_category),
            MetricOption(label="Mood Swings", category=mood_category),
            MetricOption(label="Irritated", category=mood_category),
            MetricOption(label="Sad", category=mood_category),
            MetricOption(label="Anxious", category=mood_category),
            MetricOption(label="Depressed", category=mood_category),
            MetricOption(label="Guilty", category=mood_category),
            MetricOption(label="Low Energy", category=mood_category),
            MetricOption(label="Apathetic", category=mood_category),
            MetricOption(label="Confused", category=mood_category),
            MetricOption(label="Self-critical", category=mood_category),
            MetricOption(label="Cramps", category=symptom_category),
            MetricOption(label="Headache", category=symptom_category),
            MetricOption(label="Acne", category=symptom_category),
            MetricOption(label="Backache", category=symptom_category),
            MetricOption(label="Fatigue", category=symptom_category),
            MetricOption(label="Cravings", category=symptom_category),
            MetricOption(label="Insomnia", category=symptom_category),
            MetricOption(label="Abdominal pain", category=symptom_category),
            MetricOption(label="Bleeding Gums", category=symptom_category),
            MetricOption(label="Food aversions", category=appetite_category),
            MetricOption(label="Increased appetite", category=appetite_category),
            MetricOption(label="Decreased appetite", category=appetite_category),
            MetricOption(label="Limbs swelling", category=swelling_category),
            MetricOption(label="Face swelling", category=swelling_category),
            MetricOption(label="Nasal congestion", category=swelling_category),
            MetricOption(label="Yoga", category=physical_activity_category),
            MetricOption(label="Gym", category=physical_activity_category),
            MetricOption(label="Swimming", category=physical_activity_category),
            MetricOption(label="Aerobics", category=physical_activity_category),
            MetricOption(label="Dancing", category=physical_activity_category),
            MetricOption(label="Running", category=physical_activity_category),
            MetricOption(label="Walking", category=physical_activity_category),
            MetricOption(label="Cycling", category=physical_activity_category),
            MetricOption(label="Team sports", category=physical_activity_category),
            MetricOption(label="Travel", category=others_category),
            MetricOption(label="Stress", category=others_category),
            MetricOption(label="Disease", category=others_category),
            MetricOption(label="Injury", category=others_category),
            MetricOption(label="Alcohol", category=others_category),
        ]
        for metric_option in all_metric_options:
            db.add(metric_option)

        db.commit()
        return all_metric_options
