import httpx
import pytest

from app.db.db_schema import PregnantWoman


@pytest.mark.asyncio
async def test_get_journal_entry_pass(
    authenticated_pregnant_woman_client: tuple[httpx.AsyncClient, PregnantWoman],
    # db_session: AsyncSession,
) -> None:
    pass
    # client, mother = authenticated_pregnant_woman_client

    # journal_entry_content: str = "Test journal entry content"
    # journal_entry_date: date = date.today() - timedelta(days=3)

    # entry = JournalEntry(
    #     author_id=mother.id,
    #     content=journal_entry_content,
    #     logged_on=journal_entry_date,
    # )
    # db_session.add(entry)
    # await db_session.commit()

    # response = client.get("/journals/")
    # assert response.status_code == status.HTTP_200_OK, "Retrieving journal entries should succeed with 200 OK"

    # data = response.json()
    # assert len(data) == 1, "There should be one journal entry returned"

    # retrieved_entry = data[0]
    # assert retrieved_entry["content"] == "Test journal entry content", (
    #     "Journal entry content should match the created entry"
    # )
    # assert retrieved_entry["logged_on"] == journal_entry_date.isoformat(), (
    #     "Journal entry date should match the created entry"
    # )


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
