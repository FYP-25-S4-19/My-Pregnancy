from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import PregnantWoman
from app.features.journal.journal_models import GetJournalEntryResponse, UpsertJournalEntryRequest
from app.features.journal.journal_service import JournalService

journal_router = APIRouter(prefix="/journal")


def get_journal_service(db: Session = Depends(get_db)) -> JournalService:
    return JournalService(db)


@journal_router.get("/", response_model=list[GetJournalEntryResponse])
def get_all_journal_entries_for_mother(
    mother: PregnantWoman = Depends(require_role(PregnantWoman)), service: JournalService = Depends(get_journal_service)
):
    return service.get_journal_entries_for_mother(mother.id)


@journal_router.put("/{entry_date}")
def upsert_journal_entry(
    entry_date: date,
    request: UpsertJournalEntryRequest,  # We'll rename this to be more generic, e.g., JournalEntryData
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
    db: Session = Depends(get_db),
    service: JournalService = Depends(get_journal_service),
):
    try:
        service.upsert_journal_entry(mother.id, entry_date, request)
        db.commit()
    except:
        db.rollback()
        raise


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
