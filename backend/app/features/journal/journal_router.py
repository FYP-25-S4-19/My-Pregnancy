from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import PregnantWoman
from app.features.journal.journal_service import JournalService

journal_router = APIRouter(prefix="/journal")


def get_journal_service(db: Session = Depends(get_db)) -> JournalService:
    return JournalService(db)


@journal_router.get("/")
def get_all_journal_entries_for_mother(
    mother: PregnantWoman = Depends(require_role(PregnantWoman)), service: JournalService = Depends(get_journal_service)
):
    return service.get_journal_entries_for_mother(mother.id)
