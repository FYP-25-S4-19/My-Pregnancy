from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import PregnantWoman
from app.features.journal.journal_models import JournalEntryResponse
from app.features.journal.journal_service import JournalService

journal_router = APIRouter(prefix="/journal")


def get_journal_service(db: Session = Depends(get_db)) -> JournalService:
    return JournalService(db)


@journal_router.get("/", response_model=list[JournalEntryResponse])
def get_all_journal_entries_for_mother(
    mother: PregnantWoman = Depends(require_role(PregnantWoman)), service: JournalService = Depends(get_journal_service)
):
    return service.get_journal_entries_for_mother(mother.id)


# @journal_router.post("/", status_code=status.HTTP_201_CREATED)
# def create_journal_entry(
#     request: JournalEntryCreateRequest,
#     mother: PregnantWoman = Depends(require_role(PregnantWoman)),
#     service: JournalService = Depends(get_journal_service),
# ):
#     pass


# @journal_router.patch("/{entry_id}")
# def edit_journal_entry(
#     entry_id: int,
#     request: JournalEntryEditRequest,
#     mother: PregnantWoman = Depends(require_role(PregnantWoman)),
#     db: Session = Depends(get_db),
#     service: JournalService = Depends(get_journal_service),
# ):
#     try:
#         service.edit_journal_entry(mother.id, entry_id, request)
#         db.commit()
#     except:
#         db.rollback()
#         raise


@journal_router.delete("/{entry_id}")
def delete_journal_entry(
    entry_id: int,
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
    db: Session = Depends(get_db),
    service: JournalService = Depends(get_journal_service),
):
    try:
        service.delete_journal_entry(mother.id, entry_id)
        db.commit()
    except:
        db.rollback()
        raise
