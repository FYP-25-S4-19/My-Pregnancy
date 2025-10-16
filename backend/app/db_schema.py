from typing import List, Optional
import enum

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Date,
    Text,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    func,
    text,
    Table,
    Column
)


class Base(DeclarativeBase):
    pass


class ConsultStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"


saved_edu_articles_table = Table(
    'saved_edu_articles',
    Base.metadata,
    Column('saver_id', ForeignKey('pregnant_women.user_id'), primary_key=True),
    Column('article_id', ForeignKey('edu_articles.id'), primary_key=True),
)


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[List['User']] = relationship(back_populates='role')


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role: Mapped[Role] = relationship(back_populates='users')

    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(60))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text('TRUE'))

    admin: Mapped[Optional['Admin']] = relationship(back_populates='user')
    volunteer_specialist: Mapped[Optional['VolunteerSpecialist']] = relationship(back_populates='user')
    pregnant_woman: Mapped[Optional['PregnantWoman']] = relationship(back_populates='user')

    community_threads: Mapped[List['CommunityThread']] = relationship(back_populates='poster')
    thread_comments: Mapped[List['ThreadComment']] = relationship(back_populates='commenter')


class Admin(Base):
    __tablename__ = 'admins'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    username: Mapped[str] = mapped_column(String(255))

    user: Mapped['User'] = relationship(back_populates='admin')


class MedicalCredentialOption(Base):
    __tablename__ = 'medical_credential_options'
    id: Mapped[int] = mapped_column(primary_key=True)
    cred_img_url: Mapped[str] = mapped_column(String(255))
    credential: Mapped[str] = mapped_column(String(50), unique=True)
    full_meaning: Mapped[str] = mapped_column(String(255), unique=True)

    specialists: Mapped[List['VolunteerSpecialist']] = relationship(back_populates='medical_credential')


class VolunteerSpecialist(Base):
    __tablename__ = 'volunteer_specialists'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))

    med_cred_id: Mapped[int] = mapped_column(ForeignKey('medical_credential_options.id'))
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=text('FALSE'))

    user: Mapped['User'] = relationship(back_populates='volunteer_specialist')
    medical_credential: Mapped[MedicalCredentialOption] = relationship(back_populates='specialists')

    consultations_as_specialist: Mapped[List['Consultation']] = relationship(
        foreign_keys='Consultation.specialist_id', back_populates='specialist'
    )

    saved_by: Mapped[List['SavedVolunteerSpecialist']] = relationship(back_populates='specialist')


class PregnantWoman(Base):
    __tablename__ = 'pregnant_women'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    profile_img_url: Mapped[str | None] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    due_date: Mapped[Date | None] = mapped_column(Date)

    user: Mapped['User'] = relationship(back_populates='pregnant_woman')

    consultations_as_mother: Mapped[List['Consultation']] = relationship(
        foreign_keys='Consultation.mother_id', back_populates='mother'
    )

    saved_articles: Mapped[List['EduArticle']] = relationship(
        secondary=saved_edu_articles_table, back_populates='savers'
    )

    saved_specialists_links: Mapped[List['SavedVolunteerSpecialist']] = relationship(back_populates='mother')

    metric_logs: Mapped[List['MetricLog']] = relationship(back_populates='pregnant_woman')
    journal_entries: Mapped[List['JournalEntry']] = relationship(back_populates='author')
    bump_entries: Mapped[List['BumpEntry']] = relationship(back_populates='uploader')


# ----- EDUCATIONAL CONTENT -----
class EduArticleCategory(Base):
    __tablename__ = 'edu_article_categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255), unique=True)

    articles: Mapped[List['EduArticle']] = relationship(back_populates='category')


class EduArticle(Base):
    __tablename__ = 'edu_articles'
    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('edu_article_categories.id'))
    category: Mapped[EduArticleCategory] = relationship(back_populates='articles')

    img_url: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    content_markdown: Mapped[str] = mapped_column(Text)

    savers: Mapped[List[PregnantWoman]] = relationship(
        secondary=saved_edu_articles_table, back_populates='saved_articles'
    )


# ------ CONSULTATIONS -------
class SavedVolunteerSpecialist(Base):
    __tablename__ = 'saved_volunteer_specialists'

    saver_id: Mapped[int] = mapped_column(ForeignKey('pregnant_women.user_id'), primary_key=True)
    specialist_id: Mapped[int] = mapped_column(ForeignKey('volunteer_specialists.user_id'), primary_key=True)

    mother: Mapped['PregnantWoman'] = relationship(back_populates='saved_specialists_links')
    specialist: Mapped['VolunteerSpecialist'] = relationship(back_populates='saved_by')


class Consultation(Base):
    __tablename__ = 'consultations'
    id: Mapped[int] = mapped_column(primary_key=True)

    specialist_id: Mapped[int] = mapped_column(ForeignKey('volunteer_specialists.user_id'))
    mother_id: Mapped[int] = mapped_column(ForeignKey('pregnant_women.user_id'))

    start_time: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[ConsultStatus] = mapped_column(SQLAlchemyEnum(ConsultStatus))

    specialist: Mapped[VolunteerSpecialist] = relationship(
        foreign_keys=[specialist_id],
        back_populates='consultations_as_specialist'
    )
    mother: Mapped[PregnantWoman] = relationship(
        foreign_keys=[mother_id],
        back_populates='consultations_as_mother'
    )


# ----- METRIC (MOOD, SYMPTOM) TRACKER + JOURNAL ------
class MetricCategory(Base):
    __tablename__ = 'metric_categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255), unique=True)

    options: Mapped[List['MetricOption']] = relationship(back_populates='category')


class MetricOption(Base):
    __tablename__ = 'metric_options'
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('metric_categories.id'))

    category: Mapped[MetricCategory] = relationship(back_populates='options')
    logs: Mapped[List['MetricLog']] = relationship(back_populates='metric_option')


class MetricLog(Base):
    __tablename__ = 'metric_logs'
    user_id: Mapped[int] = mapped_column(ForeignKey('pregnant_women.user_id'), primary_key=True)
    metric_option_id: Mapped[int] = mapped_column(ForeignKey('metric_options.id'), primary_key=True)
    logged_at: Mapped[DateTime] = mapped_column(DateTime, primary_key=True)

    pregnant_woman: Mapped[PregnantWoman] = relationship(back_populates='metric_logs')
    metric_option: Mapped[MetricOption] = relationship(back_populates='logs')


class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('pregnant_women.user_id'))
    content: Mapped[str] = mapped_column(Text)
    date: Mapped[Date] = mapped_column(Date)

    author: Mapped[PregnantWoman] = relationship(back_populates='journal_entries')


class BumpEntry(Base):
    __tablename__ = 'bump_entries'
    id: Mapped[int] = mapped_column(primary_key=True)
    uploader_id: Mapped[int] = mapped_column(ForeignKey('pregnant_women.user_id'))
    bump_img_url: Mapped[str] = mapped_column(String(255))
    date: Mapped[Date] = mapped_column(Date)

    uploader: Mapped[PregnantWoman] = relationship(back_populates='bump_entries')


# ----- COMMUNITY FORUM -------
class CommunityThread(Base):
    __tablename__ = 'community_thread'
    id: Mapped[int] = mapped_column(primary_key=True)
    poster_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    posted_at: Mapped[DateTime] = mapped_column(DateTime)

    poster: Mapped[User] = relationship(back_populates='community_threads')
    comments: Mapped[List['ThreadComment']] = relationship(back_populates='thread')


class ThreadComment(Base):
    __tablename__ = 'thread_comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey('community_thread.id'))
    commenter_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(Text)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, server_default=text('FALSE'))

    thread: Mapped[CommunityThread] = relationship(back_populates='comments')
    commenter: Mapped[User | None] = relationship(back_populates='thread_comments')