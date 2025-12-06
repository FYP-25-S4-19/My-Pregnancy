from fastapi import APIRouter, Depends, HTTPException, status

# from getstream import Stream
# from getstream.models import UserRequest
from stream_chat import StreamChat

from app.core.settings import settings
from app.core.users_manager import current_active_user
from app.db.db_schema import User
from app.shared.utils import format_user_fullname

stream_router = APIRouter(prefix="/stream", tags=["GetStream"])


def get_server_client():
    if not settings.STREAM_API_KEY or not settings.STREAM_API_SECRET:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)


@stream_router.get("/token")
async def get_stream_token(user: User = Depends(current_active_user)):
    server_client: StreamChat = get_server_client()
    token: str = server_client.create_token(str(user.id))
    try:
        server_client.upsert_user({"id": str(user.id), "name": format_user_fullname(user)})
        return {"token": token}
    except Exception as e:
        print("Error while fetching stream token:", e)
        raise


# @stream_router.post("/chat/channel")
# async def create_chat_channel(args: ChannelCreationArgs, mother: PregnantWoman = Depends(require_role(PregnantWoman))):
#     # TODO: Logic for checking if there already exists a channel between this pair of "Doctor" and "Mother"
#     server_client: StreamChat = get_server_client()


# @stream_router.post("/chat/channel/message")
# async def send_message(user: User = Depends(require_role(User))):
#     server_client: StreamChat = get_server_client()
# server_client.send_mes
