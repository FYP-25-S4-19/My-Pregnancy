from app.core.custom_base_model import CustomBaseModel


class ThreadPreview(CustomBaseModel):
    id: int
    creator_name: str
    title: str
    content: str
    posted_at: str
