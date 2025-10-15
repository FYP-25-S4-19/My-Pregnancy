import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Date,
    Text,
    Enum as SQLAlchemyEnum,
    Table
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

# --- Base Configuration ---
Base = declarative_base()


# --- Custom ENUM Type ---
class ConsultStatusEnum(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"
# =================================================================
# ---- USER MANAGEMENT -----
# =================================================================
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False, unique=True)  # e.g., "admin", "specialist", "mother"

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    role = relationship("Role", back_populates="users")

    # One-to-One relationships to profile tables
    admin_profile = relationship("Admin", back_populates="user", uselist=False)
    specialist_profile = relationship("VolunteerSpecialist", back_populates="user", uselist=False)
    pregnant_woman_profile = relationship("PregnantWoman", back_populates="user", uselist=False)

    # One-to-Many for forum posts
    threads_posted = relationship("CommunityThread", back_populates="poster")
    comments_posted = relationship("ThreadComment", back_populates="commenter")


# --- Profile Tables ---
class Admin(Base):
    __tablename__ = "admins"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    username = Column(String(100), nullable=False)
    user = relationship("User", back_populates="admin_profile")


class VolunteerSpecialist(Base):
    __tablename__ = "volunteer_specialists"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    med_cred_id = Column(Integer, ForeignKey("medical_credential_options.id"), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="specialist_profile")
    credential = relationship("MedicalCredentialOption", back_populates="specialists")
    consultations = relationship("Consultation", back_populates="specialist")
    saved_by_users = relationship("PregnantWoman", secondary="saved_volunteer_specialists",
                                  back_populates="saved_specialists")


class PregnantWoman(Base):
    __tablename__ = "pregnant_women"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    profile_img_url = Column(String)
    username = Column(String(100), nullable=False)
    due_date = Column(Date)

    user = relationship("User", back_populates="pregnant_woman_profile")

    # Relationships to user-specific content
    consultations = relationship("Consultation", back_populates="mother")
    metric_logs = relationship("MetricLog", back_populates="user")
    journal_entries = relationship("JournalEntry", back_populates="author")
    bump_entries = relationship("BumpEntry", back_populates="uploader")

    # Many-to-Many relationships
    saved_articles = relationship("EduArticle", secondary="saved_edu_articles", back_populates="saved_by_users")
    saved_specialists = relationship("VolunteerSpecialist", secondary="saved_volunteer_specialists",
                                     back_populates="saved_by_users")


# =================================================================
# ---- MANY-TO-MANY ASSOCIATION TABLES ----
# =================================================================

saved_edu_articles_association = Table(
    "saved_edu_articles",
    Base.metadata,
    Column("saver_id", Integer, ForeignKey("pregnant_women.user_id"), primary_key=True),
    Column("article_id", Integer, ForeignKey("edu_articles.id"), primary_key=True),
)

saved_volunteer_specialists_association = Table(
    "saved_volunteer_specialists",
    Base.metadata,
    Column("saver_id", Integer, ForeignKey("pregnant_women.user_id"), primary_key=True),
    Column("specialist_id", Integer, ForeignKey("volunteer_specialists.user_id"), primary_key=True),
)


# =================================================================
# ---- EDUCATIONAL CONTENT & MISC ----
# =================================================================

class EduArticleCategory(Base):
    __tablename__ = "edu_article_categories"
    id = Column(Integer, primary_key=True)
    label = Column(String(100), unique=True, nullable=False)
    articles = relationship("EduArticle", back_populates="category")


class EduArticle(Base):
    __tablename__ = "edu_articles"
    id = Column(Integer, primary_key=True)
    # NOTE: Your schema had `varchar`, fixed to Integer FK
    category_id = Column(Integer, ForeignKey("edu_article_categories.id"), nullable=False)
    img_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content_markdown = Column(Text, nullable=False)
    week = Column(Integer)  # e.g., for week-specific recommendations

    category = relationship("EduArticleCategory", back_populates="articles")
    saved_by_users = relationship("PregnantWoman", secondary="saved_edu_articles", back_populates="saved_articles")


class MedicalCredentialOption(Base):
    __tablename__ = "medical_credential_options"
    id = Column(Integer, primary_key=True)
    cred_img_url = Column(String, nullable=False)
    credential = Column(String(20), unique=True, nullable=False)  # e.g., "M.D."
    full_meaning = Column(String, unique=True, nullable=False)  # e.g., "Doctor of Medicine"

    specialists = relationship("VolunteerSpecialist", back_populates="credential")


# =================================================================
# ---- CONSULTATIONS & TRACKING ----
# =================================================================

class Consultation(Base):
    __tablename__ = "consultations"
    id = Column(Integer, primary_key=True)
    specialist_id = Column(Integer, ForeignKey("volunteer_specialists.user_id"), nullable=False)
    mother_id = Column(Integer, ForeignKey("pregnant_women.user_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(ConsultStatusEnum))

    specialist = relationship("VolunteerSpecialist", back_populates="consultations")
    mother = relationship("PregnantWoman", back_populates="consultations")


class MetricCategory(Base):
    __tablename__ = "metric_categories"
    id = Column(Integer, primary_key=True)
    label = Column(String(100), unique=True, nullable=False)
    options = relationship("MetricOption", back_populates="category")


class MetricOption(Base):
    __tablename__ = "metric_options"
    id = Column(Integer, primary_key=True)
    label = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("metric_categories.id"), nullable=False)

    category = relationship("MetricCategory", back_populates="options")
    logs = relationship("MetricLog", back_populates="metric_option")


class MetricLog(Base):
    __tablename__ = "metric_logs"
    user_id = Column(Integer, ForeignKey("pregnant_women.user_id"), primary_key=True)
    metric_option_id = Column(Integer, ForeignKey("metric_options.id"), primary_key=True)
    logged_at = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())

    user = relationship("PregnantWoman", back_populates="metric_logs")
    metric_option = relationship("MetricOption", back_populates="logs")


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("pregnant_women.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(Date, nullable=False)

    author = relationship("PregnantWoman", back_populates="journal_entries")


class BumpEntry(Base):
    __tablename__ = "bump_entries"
    id = Column(Integer, primary_key=True)
    uploader_id = Column(Integer, ForeignKey("pregnant_women.user_id"), nullable=False)
    bump_img_url = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    uploader = relationship("PregnantWoman", back_populates="bump_entries")


# =================================================================
# ---- COMMUNITY FORUM ----
# =================================================================

class CommunityThread(Base):
    __tablename__ = "community_thread"
    id = Column(Integer, primary_key=True)
    poster_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    posted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    poster = relationship("User", back_populates="threads_posted")
    comments = relationship("ThreadComment", back_populates="thread")


class ThreadComment(Base):
    __tablename__ = "thread_comments"
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey("community_thread.id"), nullable=False)
    commenter_id = Column(Integer, ForeignKey("users.id"))  # Nullable if anonymous is truly anon
    content = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=False, nullable=False)

    thread = relationship("CommunityThread", back_populates="comments")
    commenter = relationship("User", back_populates="comments_posted")