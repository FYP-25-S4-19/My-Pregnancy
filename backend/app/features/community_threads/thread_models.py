from datetime import datetime

from app.core.custom_base_model import CustomBaseModel


class ThreadPreviewData(CustomBaseModel):
    id: int
    creator_name: str
    title: str
    content: str
    posted_at: str


class ThreadCommentData(CustomBaseModel):
    id: int

    thread_id: int
    commenter_id: int
    commenter_fullname: str

    commented_at: datetime
    content: str


class ThreadData(CustomBaseModel):
    id: int

    creator_id: int
    creator_fullname: str

    title: str
    content: str
    posted_at: datetime

    comments: list[ThreadCommentData]


class CreateThreadData(CustomBaseModel):
    title: str
    content: str


class ThreadUpdateData(CustomBaseModel):
    title: str
    content: str
