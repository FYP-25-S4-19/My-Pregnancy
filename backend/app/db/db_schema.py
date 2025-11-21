from __future__ import annotations

from datetime import date, datetime
from enum import Enum, IntEnum

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    text,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AppointmentStatus(Enum):
    PENDING_ACCEPT_REJECT = "PENDING_ACCEPT_REJECT"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"


class UserRole(Enum):
    ADMIN = "ADMIN"
    VOLUNTEER_DOCTOR = "VOLUNTEER_DOCTOR"
    PREGNANT_WOMAN = "PREGNANT_WOMAN"
    NUTRITIONIST = "NUTRITIONIST"


class BinaryMetricCategory(Enum):
    MOOD = "MOOD"
    SYMPTOMS = "SYMPTOMS"
    APPETITE = "APPETITE"
    DIGESTION = "DIGESTION"
    SWELLING = "SWELLING"
    PHYSICAL_ACTIVITY = "PHYSICAL_ACTIVITY"
    OTHERS = "OTHERS"


class DoctorQualificationOption(IntEnum):
    MD = 1
    DO = 2
    MBBS = 3
    MBChB = 4
    BMed = 5
    BM = 6


class NutritionistQualificationOption(IntEnum):
    BSC_NUTRITION = 1
    BSC_DIETETICS = 2
    MSC_NUTRITION = 3
    MSC_DIETETICS = 4
    RD = 5
    RDN = 6
    CNS = 7
    DIPLOMA_CLINICAL_NUTRITION = 8
    DIPLOMA_NUTRITION = 9
    CERTIFIED_NUTRITIONIST = 10


class EduArticleCategory(Enum):
    NUTRITION = "NUTRITION"
    BODY = "BODY"
    BABY = "BABY"
    FEEL_GOOD = "FEEL_GOOD"
    MEDICAL = "MEDICAL"
    EXERCISE = "EXERCISE"
    LABOUR = "LABOUR"
    LIFESTYLE = "LIFESTYLE"
    RELATIONSHIPS = "RELATIONSHIPS"


class NotificationType(Enum):
    THREAD_LIKE = "THREAD_LIKE"  # Someone liked a thread you made
    THREAD_COMMENT = "THREAD_COMMENT"  # Someone commented on a thread you made
    COMMENT_LIKE = "COMMENT_LIKE"  # Someone liked a comment you wrote
    COMMENT_REPLY = "COMMENT_REPLY"  # Someone replied to a comment you wrote
    NEW_ARTICLE = "NEW_ARTICLE"  # A new article (that you might like) was posted
    APPOINTMENT_REMINDER = "APPOINTMENT_REMINDER"
    APPOINTMENT_REQUEST = "APPOINTMENT_REQUEST"
    PRIVATE_MESSAGE = "PRIVATE_MESSAGE"


# ===========================================
# ============= GENERAL USER ================
# ===========================================
class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "type"}
    type: Mapped[str]

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    profile_img_key: Mapped[str | None]

    role: Mapped["UserRole"] = mapped_column(SQLAlchemyEnum(UserRole))

    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(server_default=text("TRUE"))

    threads_created: Mapped[list["CommunityThread"]] = relationship(back_populates="creator")
    thread_comments: Mapped[list["ThreadComment"]] = relationship(back_populates="commenter")
    threads_liked: Mapped[list["CommunityThreadLike"]] = relationship(back_populates="liker")
    feedback_given: Mapped["UserAppFeedback"] = relationship(back_populates="author")
    saved_edu_articles: Mapped[list["SavedEduArticle"]] = relationship(back_populates="saver")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="recipient")


class Admin(User):
    __tablename__ = "admins"
    __mapper_args__ = {"polymorphic_identity": "admin"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class VolunteerDoctor(User):
    __tablename__ = "volunteer_doctors"
    __mapper_args__ = {"polymorphic_identity": "volunteer_doctor"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # For all other subclasses of the base "User", they may use just "username"
    # However, it would be more professional for Doctors & Nutritionists to have their full names available
    first_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[str | None] = mapped_column(String(64))  # Middle name optional
    last_name: Mapped[str] = mapped_column(String(64))

    # Linking to their specific instance of their creds in the "medical credentials" table
    qualification_id: Mapped[int] = mapped_column(ForeignKey("doctor_qualifications.id"))
    qualification: Mapped["DoctorQualification"] = relationship(back_populates="doctor")

    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))

    # Keep track of the "Pregnant Women" who have "saved" you
    saved_by: Mapped[list["SavedVolunteerDoctor"]] = relationship(back_populates="volunteer_doctor")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="volunteer_doctor")

    articles_written: Mapped[list["EduArticle"]] = relationship(back_populates="author")


class PregnantWoman(User):
    __tablename__ = "pregnant_women"
    __mapper_args__ = {"polymorphic_identity": "pregnant_woman"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    due_date: Mapped[date | None]  # Nullable (may not be expecting)

    saved_volunteer_doctors: Mapped[list["SavedVolunteerDoctor"]] = relationship(back_populates="mother")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="mother")
    journal_entries: Mapped[list["JournalEntry"]] = relationship(back_populates="author")
    # bump_entries: Mapped[list["BumpEntry"]] = relationship(back_populates="uploader")
    kick_tracker_sessions: Mapped[list["KickTrackerSession"]] = relationship(back_populates="mother")


class Nutritionist(User):
    __tablename__ = "nutritionists"
    __mapper_args__ = {"polymorphic_identity": "nutritionist"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # For all other subclasses of the base "User", they may use just "username"
    # However, it would be more professional for Doctors & Nutritionists to have their full names available
    first_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[str | None] = mapped_column(String(64))  # Middle name optional
    last_name: Mapped[str] = mapped_column(String(64))

    # Linking to their specific instance of their creds in the "medical credentials" table
    qualification_id: Mapped[int] = mapped_column(ForeignKey("nutritionist_qualifications.id"))
    qualification: Mapped["NutritionistQualification"] = relationship(back_populates="nutritionist")

    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    recipes_created: Mapped[list["Recipe"]] = relationship(back_populates="nutritionist")


# ==================================================
# ================ QUALIFICATIONS ==================
# ==================================================


# The actual INSTANCES of "Medical Qualification" - Each VolunteerDoctor should have one!
class DoctorQualification(Base):
    __tablename__ = "doctor_qualifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    qualification_img_key: Mapped[str | None]
    qualification_option: Mapped["DoctorQualificationOption"] = mapped_column(SQLAlchemyEnum(DoctorQualificationOption))

    # The specific "doctor" that this credential is mapped to
    doctor: Mapped["VolunteerDoctor"] = relationship(back_populates="qualification")


# The actual INSTANCES of "Nutritionist Qualification" - Each Nutritionist should have one!
class NutritionistQualification(Base):
    __tablename__ = "nutritionist_qualifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    qualification_img_key: Mapped[str | None]
    qualification_option: Mapped["NutritionistQualificationOption"] = mapped_column(
        SQLAlchemyEnum(NutritionistQualificationOption)
    )

    # The specific "nutritionist" that this credential is mapped to
    nutritionist: Mapped["Nutritionist"] = relationship(back_populates="qualification")


# ================================================
# =========== EDUCATIONAL CONTENT ================
# ================================================
class EduArticle(Base):
    __tablename__ = "edu_articles"
    id: Mapped[int] = mapped_column(primary_key=True)

    # >Nullable
    # Just in case we pull external articles, and they DON'T link
    # to one of the Doctors within our database
    author_id: Mapped[int | None] = mapped_column(ForeignKey("volunteer_doctors.id"))
    author: Mapped["VolunteerDoctor"] = relationship(back_populates="articles_written")

    # Each article has exactly 1 category (for now)
    category: Mapped["EduArticleCategory"] = mapped_column(SQLAlchemyEnum(EduArticleCategory))

    img_key: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255), unique=True)
    content_markdown: Mapped[str] = mapped_column(Text)

    # Keep track of which users "saved" you
    saved_edu_articles: Mapped[list["SavedEduArticle"]] = relationship(back_populates="article")


class SavedEduArticle(Base):
    __tablename__ = "saved_edu_articles"
    saver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    saver: Mapped["User"] = relationship(back_populates="saved_edu_articles")

    article_id: Mapped[int] = mapped_column(ForeignKey("edu_articles.id"), primary_key=True)
    article: Mapped["EduArticle"] = relationship(back_populates="saved_edu_articles")


# ========================================================
# ================ MISC ASSOC TABLES =====================
# ========================================================


# Association table for a "Pregnant Woman" who saves a "Volunteer Doctor"
# Composite primary key
class SavedVolunteerDoctor(Base):
    __tablename__ = "saved_volunteer_doctors"

    mother_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"), primary_key=True)
    mother: Mapped["PregnantWoman"] = relationship(back_populates="saved_volunteer_doctors")

    volunteer_doctor_id: Mapped[int] = mapped_column(ForeignKey("volunteer_doctors.id"), primary_key=True)
    volunteer_doctor: Mapped["VolunteerDoctor"] = relationship(back_populates="saved_by")


# Association table for a "Pregnant Woman" who creates an "appointment request"
class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    volunteer_doctor_id: Mapped[int] = mapped_column(ForeignKey("volunteer_doctors.id"))
    volunteer_doctor: Mapped[VolunteerDoctor] = relationship(back_populates="appointments")

    mother_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"))
    mother: Mapped[PregnantWoman] = relationship(back_populates="appointments")

    start_time: Mapped[datetime]
    status: Mapped[AppointmentStatus] = mapped_column(SQLAlchemyEnum(AppointmentStatus))


# ===========================================================
# ========== JOURNAL | METRICS (MOOD, SYMPTOM) ==============
# ===========================================================
class BinaryMetric(Base):
    __tablename__ = "binary_metrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255), unique=True)

    # Each "Metric Option" will have a "Metric Category".
    # "Happy" -> Mood
    # "Leg cramps" -> Symptoms
    # etc....
    # category_id: Mapped[int] = mapped_column(ForeignKey("binary_metric_categories.id"))
    category: Mapped["BinaryMetricCategory"] = mapped_column(SQLAlchemyEnum(BinaryMetricCategory))

    # The "Metric Logs" in "Journal Entries" that are making use of the current option
    journal_binary_metric_logs: Mapped[list["JournalBinaryMetricLog"]] = relationship(back_populates="binary_metric")


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"))
    author: Mapped["PregnantWoman"] = relationship(back_populates="journal_entries")

    content: Mapped[str] = mapped_column(Text)
    logged_on: Mapped[date]

    # NOTE: The actual chosen options are inside each "Metric Log"
    journal_binary_metric_logs: Mapped[list["JournalBinaryMetricLog"]] = relationship(back_populates="journal_entry")
    journal_scalar_metric_logs: Mapped[list["JournalScalarMetricLog"]] = relationship(back_populates="journal_entry")
    journal_blood_pressure_logs: Mapped[list["JournalBloodPressureLog"]] = relationship(back_populates="journal_entry")


# Association table associating a "Journal Entry" with a "Binary Metric"
# i.e. Everytime you log a "Journal Entry", you may have multiple "Binary Metrics" associated with it
#
# Composite primary key
class JournalBinaryMetricLog(Base):
    __tablename__ = "journal_binary_metric_logs"

    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), primary_key=True)
    journal_entry: Mapped["JournalEntry"] = relationship(back_populates="journal_binary_metric_logs")

    binary_metric_id: Mapped[int] = mapped_column(ForeignKey("binary_metrics.id"), primary_key=True)
    binary_metric: Mapped["BinaryMetric"] = relationship(back_populates="journal_binary_metric_logs")


class ScalarMetric(Base):
    __tablename__ = "scalar_metrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(128), unique=True)
    unit_of_measurement: Mapped[str] = mapped_column(String(128), unique=True)  # Systolic, Litres, Kilograms, etc...
    journal_scalar_metric_logs: Mapped[list["JournalScalarMetricLog"]] = relationship(back_populates="scalar_metric")


class JournalScalarMetricLog(Base):
    __tablename__ = "journal_scalar_metric_logs"

    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), primary_key=True)
    journal_entry: Mapped["JournalEntry"] = relationship(back_populates="journal_scalar_metric_logs")

    scalar_metric_id: Mapped[int] = mapped_column(ForeignKey("scalar_metrics.id"), primary_key=True)
    scalar_metric: Mapped["ScalarMetric"] = relationship(back_populates="journal_scalar_metric_logs")

    value: Mapped[float]


class JournalBloodPressureLog(Base):
    __tablename__ = "journal_blood_pressure_logs"

    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), primary_key=True)
    journal_entry: Mapped["JournalEntry"] = relationship(back_populates="journal_blood_pressure_logs")

    systolic: Mapped[int]
    diastolic: Mapped[int]


# class BumpEntry(Base):
#     __tablename__ = "bump_entries"
#     id: Mapped[int] = mapped_column(primary_key=True)
#
#     uploader_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"))
#     uploader: Mapped["PregnantWoman"] = relationship(back_populates="bump_entries")
#
#     bump_img_key: Mapped[str] = mapped_column(String(255))
#     date: Mapped[date]


# ============================================
# ============ COMMUNITY FORUM ===============
# ============================================
# A 'thread' is what you would usually call a 'forum post'
#
# I hesitated to call it 'post', just because of possible weird names that would
# potentially arise when having to use this in conjunction with the HTTP "POST" method
class CommunityThread(Base):
    __tablename__ = "community_threads"
    id: Mapped[int] = mapped_column(primary_key=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="threads_created")

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    posted_at: Mapped[datetime]

    comments: Mapped[list["ThreadComment"]] = relationship(back_populates="thread")
    community_thread_likes: Mapped[list["CommunityThreadLike"]] = relationship(back_populates="thread")


# An association table for when a "user" likes a "community thread"
class CommunityThreadLike(Base):
    __tablename__ = "community_thread_likes"

    liker_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    liker: Mapped["User"] = relationship(back_populates="threads_liked")

    thread_id: Mapped[int] = mapped_column(ForeignKey("community_threads.id"), primary_key=True)
    thread: Mapped["CommunityThread"] = relationship(back_populates="community_thread_likes")


class ThreadComment(Base):
    __tablename__ = "thread_comments"
    id: Mapped[int] = mapped_column(primary_key=True)

    thread_id: Mapped[int] = mapped_column(ForeignKey("community_threads.id"))
    thread: Mapped["CommunityThread"] = relationship(back_populates="comments")

    commenter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commenter: Mapped["User"] = relationship(back_populates="thread_comments")

    commented_at: Mapped[datetime]
    content: Mapped[str] = mapped_column(Text)


# ============================================
# =============== RECIPES ====================
# ============================================
class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)

    nutritionist_id: Mapped[int] = mapped_column(ForeignKey("nutritionists.id"))
    nutritionist: Mapped["Nutritionist"] = relationship(back_populates="recipes_created")

    name: Mapped[str]
    img_key: Mapped[str | None]
    prepare_time_minutes: Mapped[int]
    serving_count: Mapped[int]
    instructions: Mapped[str]
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    protein_per_100g: Mapped[float | None]
    carbs_per_100g: Mapped[float | None]
    fats_per_100g: Mapped[float | None]
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(back_populates="ingredient")


# The actual association table linking "recipe" and "ingredient"
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")

    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipe_ingredients")

    amount: Mapped[int]
    unit_of_measurement: Mapped[str]


# ===========================================
# ============= KICK TRACKER ================
# ===========================================
class KickTrackerSession(Base):
    __tablename__ = "kick_tracker_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)

    mother_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"))
    mother: Mapped["PregnantWoman"] = relationship(back_populates="kick_tracker_sessions")

    started_at: Mapped[datetime]
    ended_at: Mapped[datetime]
    kicks: Mapped[list["KickTrackerKicks"]] = relationship(back_populates="session")


class KickTrackerKicks(Base):
    __tablename__ = "kick_tracker_kicks"
    id: Mapped[int] = mapped_column(primary_key=True)
    kick_at: Mapped[datetime]

    session_id: Mapped[int] = mapped_column(ForeignKey("kick_tracker_sessions.id"))
    session: Mapped["KickTrackerSession"] = relationship(back_populates="kicks")


# ===========================================
# ============ MISCELLANEOUS ================
# ===========================================
class UserAppFeedback(Base):
    __tablename__ = "user_app_feedback"
    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="feedback_given")

    rating: Mapped[int]
    content: Mapped[str]


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)

    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient: Mapped["User"] = relationship(back_populates="notifications")

    content: Mapped[str]
    sent_at: Mapped[datetime]

    # Intention - at the time of writing - is for the application layer to mark
    # a notification as "seen" once you click it
    #
    # I'll just assume that all the "seen" ones can be soft-deleted
    # Perhaps an occasional job can be run on the server to hard-delete those marked as seen
    is_seen: Mapped[bool] = mapped_column(server_default=text("FALSE"))

    # ----- Type + Data -----
    # For use at the application layer. Perhaps the type can dictate where you are led to when the app is clicked
    # type = "article", data = "45" (i.e. New suggested article, click to go to article ID=45)
    # type = "message_reply", data = "<SOME_JSON_DATA>" (i.e. JSON object containing link to message)
    type: Mapped["NotificationType"] = mapped_column(SQLAlchemyEnum(NotificationType))
    data: Mapped[str]


class ExpoPushToken(Base):
    __tablename__ = "expo_push_tokens"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    token: Mapped[str]
