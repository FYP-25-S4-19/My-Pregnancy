from uuid import UUID

from app.core.custom_base_model import CustomBaseModel


class TokenResponse(CustomBaseModel):
    token: str


class ChannelCreationArgs(CustomBaseModel):
    doctor_id: UUID


class StreamChatMessage(CustomBaseModel):
    channel_id: str
    text: str
