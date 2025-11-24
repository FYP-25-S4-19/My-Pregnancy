from datetime import date, timedelta

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.db_schema import JournalEntry, PregnantWoman


def test_get_journal_entry_pass(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman], db_session: Session
) -> None:
    client, mother = authenticated_pregnant_woman_client

    JOURNAL_ENTRY_CONTENT: str = "Test journal entry content"
    JOURNAL_ENTRY_DATE: date = date.today() - timedelta(days=3)

    entry = JournalEntry(
        author_id=mother.id,
        content=JOURNAL_ENTRY_CONTENT,
        logged_on=JOURNAL_ENTRY_DATE,
    )
    db_session.add(entry)
    db_session.commit()

    response = client.get("/journals/")
    assert response.status_code == status.HTTP_200_OK, "Retrieving journal entries should succeed with 200 OK"

    data = response.json()
    assert len(data) == 1, "There should be one journal entry returned"

    retrieved_entry = data[0]
    assert retrieved_entry["content"] == "Test journal entry content", (
        "Journal entry content should match the created entry"
    )
    assert retrieved_entry["logged_on"] == JOURNAL_ENTRY_DATE.isoformat(), (
        "Journal entry date should match the created entry"
    )


# def test_edit_other_mother_journal(
#     authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
#     pregnant_woman: PregnantWoman,
#     db_session: Session
# ) -> None:
#     client, mother = authenticated_pregnant_woman_client
#     other_mother: PregnantWoman = pregnant_woman
#
#     JOURNAL_ENTRY_DATE: date = date.today() - timedelta(days=1)
#     journal_entry = JournalEntry(
#         author_id=other_mother.id,
#         content="Other mother's journal entry",
#         logged_on=JOURNAL_ENTRY_DATE,
#     )
#     db_session.add(journal_entry)
#     db_session.commit()
#
#     client.put("/journals/{entry_date}".format(entry_date=JOURNAL_ENTRY_DATE.isoformat()), json={})
