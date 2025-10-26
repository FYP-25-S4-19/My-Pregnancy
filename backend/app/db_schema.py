from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime, date
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
    ForeignKey,
    DateTime,
    Boolean,
    String,
    Text,
    func,
    text,
)
import enum


class Base(DeclarativeBase):
    pass


class ConsultStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"


# ===========================================
# ============= GENERAL USER ================
# ===========================================
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(50), unique=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "type"}
    type: Mapped[str]

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    profile_img_url: Mapped[str | None]

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Role] = relationship(back_populates="users")

    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("TRUE"))

    threads_created: Mapped[list["CommunityThread"]] = relationship(back_populates="creator")
    thread_comments: Mapped[list["ThreadComment"]] = relationship(back_populates="commenter")

    feedback_given: Mapped[list["UserFeedback"]] = relationship(back_populates="author")
    saved_edu_articles: Mapped[list["SavedEduArticle"]] = relationship(back_populates="saver")


class Admin(User):
    __tablename__ = "admins"
    __mapper_args__ = {"polymorphic_identity": "admin"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class VolunteerSpecialist(User):
    __tablename__ = "volunteer_specialists"
    __mapper_args__ = {"polymorphic_identity": "volunteer_specialist"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # For all other subclasses of the base "User", they may use just "username"
    # However, it would be more professional for Doctors to have their full names available
    first_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[str | None] = mapped_column(String(64))  # Middle name optional
    last_name: Mapped[str] = mapped_column(String(64))

    # Linking to their specific instance of their creds in the "medical credentials" table
    medical_credential_id: Mapped[int] = mapped_column(ForeignKey("medical_credentials.id"))
    medical_credential: Mapped["MedicalCredential"] = relationship(back_populates="credential_owner")

    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))

    # Keep track of the "Pregnant Women" who have "saved" you
    saved_by: Mapped[list["SavedVolunteerSpecialist"]] = relationship(back_populates="volunteer_specialist")
    consultations: Mapped[list["Consultation"]] = relationship(back_populates="volunteer_specialist")


class PregnantWoman(User):
    __tablename__ = "pregnant_women"
    __mapper_args__ = {"polymorphic_identity": "pregnant_woman"}
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    due_date: Mapped[date | None]  # Nullable (may not be expecting)

    saved_volunteer_specialists: Mapped[list["SavedVolunteerSpecialist"]] = relationship(back_populates="mother")
    consultations: Mapped[list["Consultation"]] = relationship(back_populates="mother")
    journal_entries: Mapped[list["JournalEntry"]] = relationship(back_populates="author")
    bump_entries: Mapped[list["BumpEntry"]] = relationship(back_populates="uploader")


# ================================================
# ============= MEDICAL CREDENTIALS ==============
# ================================================


# To be pre-seeded in the database with values such as
# "Doctor of Medicine", "Registered Nurse", "Obstetrician", "Doula", etc....
class MedicalCredentialOption(Base):
    __tablename__ = "medical_credential_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255), unique=True)

    # The instances of "Medical Credentials" that are making use of this "Medical Credential Option"
    medical_credentials: Mapped[list["MedicalCredential"]] = relationship(back_populates="credential_option")


# The actual INSTANCES of Medical Credentials - Each VolunteerSpecialist should have one!
class MedicalCredential(Base):
    __tablename__ = "medical_credentials"
    id: Mapped[int] = mapped_column(primary_key=True)
    credential_img_url: Mapped[str]

    credential_option_id: Mapped[int] = mapped_column(ForeignKey("medical_credential_options.id"))
    credential_option: Mapped["MedicalCredentialOption"] = relationship(back_populates="medical_credentials")

    # The specific "specialist" that this credential is mapped to
    credential_owner: Mapped["VolunteerSpecialist"] = relationship(back_populates="medical_credential")


# ================================================
# =========== EDUCATIONAL CONTENT ================
# ================================================
class EduArticleCategory(Base):
    __tablename__ = "edu_article_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(128), unique=True)

    # Many articles may have this category
    articles: Mapped[list["EduArticle"]] = relationship(back_populates="category")


class EduArticle(Base):
    __tablename__ = "edu_articles"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Each article has exactly 1 category (for now)
    category_id: Mapped[int] = mapped_column(ForeignKey("edu_article_categories.id"))
    category: Mapped["EduArticleCategory"] = relationship(back_populates="articles")

    img_url: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
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


# Association table for a "Pregnant Woman" who saves a "Volunteer Specialist"
# Composite primary key
class SavedVolunteerSpecialist(Base):
    __tablename__ = "saved_volunteer_specialists"

    mother_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"), primary_key=True)
    mother: Mapped["PregnantWoman"] = relationship(back_populates="saved_volunteer_specialists")

    volunteer_specialist_id: Mapped[int] = mapped_column(ForeignKey("volunteer_specialists.id"), primary_key=True)
    volunteer_specialist: Mapped["VolunteerSpecialist"] = relationship(back_populates="saved_by")


# Association table for a "Pregnant Woman" who creates a "consultation request"
# Composite primary key
class Consultation(Base):
    __tablename__ = "consultations"

    volunteer_specialist_id: Mapped[int] = mapped_column(ForeignKey("volunteer_specialists.id"), primary_key=True)
    volunteer_specialist: Mapped[VolunteerSpecialist] = relationship(back_populates="consultations")

    mother_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"), primary_key=True)
    mother: Mapped[PregnantWoman] = relationship(back_populates="consultations")

    start_time: Mapped[datetime] = mapped_column(primary_key=True)
    status: Mapped[ConsultStatus] = mapped_column(SQLAlchemyEnum(ConsultStatus))


# ===========================================================
# ========== JOURNAL | METRICS (MOOD, SYMPTOM) ==============
# ===========================================================


# There are multiple "Metric Categories" (mood, symptoms, appetite, digestion, physical activity, etc...)
# Will be pre-filled by the database
class MetricCategory(Base):
    __tablename__ = "metric_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(128), unique=True)
    metric_options: Mapped[list["MetricOption"]] = relationship(back_populates="category")


class MetricOption(Base):
    __tablename__ = "metric_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255), unique=True)

    # Each "Metric Option" will have a "Metric Category".
    # "Happy" -> Mood
    # "Leg cramps" -> Symptoms
    # etc....
    category_id: Mapped[int] = mapped_column(ForeignKey("metric_categories.id"))
    category: Mapped["MetricCategory"] = relationship(back_populates="metric_options")

    # The "Metric Logs" in "Journal Entries" that are making use of the current option
    metric_logs: Mapped[list["MetricLog"]] = relationship(back_populates="metric_option")


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"))
    author: Mapped["PregnantWoman"] = relationship(back_populates="journal_entries")

    content: Mapped[str] = mapped_column(Text)
    logged_at: Mapped[datetime]

    # NOTE: The actual chosen options are inside each "Metric Log"
    metric_logs: Mapped[list["MetricLog"]] = relationship(back_populates="journal_entry")


# Association table associating a "Journal Entry" with a "Metric Option"
# i.e. Everytime you log a "Journal Entry", you may have multiple "Metric Options" associated with it
#
# Composite primary key
class MetricLog(Base):
    __tablename__ = "metric_logs"

    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), primary_key=True)
    journal_entry: Mapped["JournalEntry"] = relationship(back_populates="metric_logs")

    metric_option_id: Mapped[int] = mapped_column(ForeignKey("metric_options.id"), primary_key=True)
    metric_option: Mapped["MetricOption"] = relationship(back_populates="metric_logs")


class BumpEntry(Base):
    __tablename__ = "bump_entries"
    id: Mapped[int] = mapped_column(primary_key=True)

    uploader_id: Mapped[int] = mapped_column(ForeignKey("pregnant_women.id"))
    uploader: Mapped["PregnantWoman"] = relationship(back_populates="bump_entries")

    bump_img_url: Mapped[str] = mapped_column(String(255))
    date: Mapped[date]


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


class ThreadComment(Base):
    __tablename__ = "thread_comments"
    id: Mapped[int] = mapped_column(primary_key=True)

    thread_id: Mapped[int] = mapped_column(ForeignKey("community_threads.id"))
    thread: Mapped["CommunityThread"] = relationship(back_populates="comments")

    commenter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commenter: Mapped["User"] = relationship(back_populates="thread_comments")

    commented_at: Mapped[datetime]
    content: Mapped[str] = mapped_column(Text)


# ===========================================
# ============ USER FEEDBACK ================
# ===========================================
class UserFeedback(Base):
    __tablename__ = "user_feedback"
    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="feedback_given")

    rating: Mapped[int]
    content: Mapped[str | None]  # Can just choose to not write anything, I suppose....
