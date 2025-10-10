from fastapi import APIRouter

items_router = APIRouter(prefix="/api/items")


@items_router.get("/")
def get_all_items() -> str:
    return "Getting all items"


@items_router.get("/{item_id}")
def get_item_by_id(item_id: int) -> str:
    return "Item of ID: " + str(item_id)
