from app.core.custom_base_model import CustomBaseModel


class ChannelCreationArgs(CustomBaseModel):
    doctor_id: int


class StreamChatMessage(CustomBaseModel):
    channel_id: str
    text: str
