from app.db_schema import User, Role, MedicalCredentialOption, MetricCategory, MetricOption, EduArticleCategory
from sqlalchemy.orm import Session


class DefaultsGenerator:
    @staticmethod
    def init_roles(db: Session):
        print("Initializing roles....")
        for role_label in ["PregnantWoman", "VolunteerSpecialist", "Admin"]:
            role = Role(label=role_label)
            db.add(role)
        db.commit()

    @staticmethod
    def init_med_cred_options(db: Session):
        print("Initializing medical credential options....")
        for cred_label in [
            "Doctor of Medicine (M.D)",
            "Doctor of Osteopathic Medicine (D.O)",
            "Licensed Midwife (LM)",
            "Obstetrician/Gynecologist (OB/GYN)",
            "Certified Nurse-Midwife (CNM)",
            "Registered Nurse (RN)",
        ]:
            cred_option = MedicalCredentialOption(label=cred_label)
            db.add(cred_option)
        db.commit()

    @staticmethod
    def init_edu_article_categories(db: Session):
        print("Initializing edu article categories.....")
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
            db.add(edu_article_category)
        db.commit()

    @staticmethod
    def init_metric_categories(db: Session):
        print("Initializing metric categories....")
        for category_label in ["Mood", "Symptoms", "Appetite", "Digestion", "Swelling", "Physical Activity", "Others"]:
            metric_category = MetricCategory(label=category_label)
            db.add(metric_category)
        db.commit()

    # Each "Metric Option" has a "Metric Category"
    # Hence, why we seed this AFTER the categories are seeded
    @staticmethod
    def init_metric_options(db: Session):
        mood_category: MetricCategory | None = db.query(MetricCategory).filter(MetricCategory.label == "Mood").first()
        symptom_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Symptoms").first()
        )
        appetite_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Appetite").first()
        )
        digestion_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Digestion").first()
        )
        swelling_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Swelling").first()
        )
        physical_activity_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Physical Activity").first()
        )
        others_category: MetricCategory | None = (
            db.query(MetricCategory).filter(MetricCategory.label == "Others").first()
        )

        db.add(MetricOption(label="Calm", category=mood_category))
        db.add(MetricOption(label="Happy", category=mood_category))
        db.add(MetricOption(label="Energetic", category=mood_category))
        db.add(MetricOption(label="Mood Swings", category=mood_category))
        db.add(MetricOption(label="Irritated", category=mood_category))
        db.add(MetricOption(label="Sad", category=mood_category))
        db.add(MetricOption(label="Anxious", category=mood_category))
        db.add(MetricOption(label="Depressed", category=mood_category))
        db.add(MetricOption(label="Guilty", category=mood_category))
        db.add(MetricOption(label="Low Energy", category=mood_category))
        db.add(MetricOption(label="Apathetic", category=mood_category))
        db.add(MetricOption(label="Confused", category=mood_category))
        db.add(MetricOption(label="Self-critical", category=mood_category))

        db.add(MetricOption(label="Cramps", category=symptom_category))
        db.add(MetricOption(label="Headache", category=symptom_category))
        db.add(MetricOption(label="Acne", category=symptom_category))
        db.add(MetricOption(label="Backache", category=symptom_category))
        db.add(MetricOption(label="Fatigue", category=symptom_category))
        db.add(MetricOption(label="Cravings", category=symptom_category))
        db.add(MetricOption(label="Insomnia", category=symptom_category))
        db.add(MetricOption(label="Abdominal pain", category=symptom_category))
        db.add(MetricOption(label="Bleeding Gums", category=symptom_category))

        db.add(MetricOption(label="Food aversions", category=appetite_category))
        db.add(MetricOption(label="Increased appetite", category=appetite_category))
        db.add(MetricOption(label="Decreased appetite", category=appetite_category))

        db.add(MetricOption(label="Limbs swelling", category=swelling_category))
        db.add(MetricOption(label="Face swelling", category=swelling_category))
        db.add(MetricOption(label="Nasal congestion", category=swelling_category))

        db.add(MetricOption(label="Yoga", category=physical_activity_category))
        db.add(MetricOption(label="Gym", category=physical_activity_category))
        db.add(MetricOption(label="Swimming", category=physical_activity_category))
        db.add(MetricOption(label="Aerobics", category=physical_activity_category))
        db.add(MetricOption(label="Dancing", category=physical_activity_category))
        db.add(MetricOption(label="Running", category=physical_activity_category))
        db.add(MetricOption(label="Walking", category=physical_activity_category))
        db.add(MetricOption(label="Cycling", category=physical_activity_category))
        db.add(MetricOption(label="Team sports", category=physical_activity_category))

        db.add(MetricOption(label="Travel", category=others_category))
        db.add(MetricOption(label="Stress", category=others_category))
        db.add(MetricOption(label="Disease", category=others_category))
        db.add(MetricOption(label="Injury", category=others_category))
        db.add(MetricOption(label="Alcohol", category=others_category))

        db.commit()
