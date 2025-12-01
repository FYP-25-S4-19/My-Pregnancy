from fastapi import APIRouter, Depends, HTTPException, status
from stream_chat import StreamChat

from app.core.settings import settings
from app.core.users_manager import current_active_user
from app.db.db_schema import User

getstream_router = APIRouter(prefix="/stream", tags=["Stream"])


def get_stream_client():
    if not settings.STREAM_API_KEY or not settings.STREAM_API_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is not configured",
        )
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)


@getstream_router.get("/token")
async def get_stream_token(user: User = Depends(current_active_user)):
    client: StreamChat = get_stream_client()
    token: str = client.create_token(str(user.id))
    try:
        client.upsert_user(
            {
                "id": str(user.id),
                "name": "".join(
                    name_part for name_part in [user.first_name, user.middle_name, user.last_name] if name_part
                ),
                # "image": user.
            }
        )
    except Exception as e:
        print(f"Failed to upsert user to Stream: {e}")

    return {"token": token, "api_key": settings.STREAM_API_KEY, "user_id": str(user.id)}
