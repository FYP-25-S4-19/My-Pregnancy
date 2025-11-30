# @pytest.mark.asyncio
# async def test_register_with_middle_name_success(client: AsyncClient) -> None:
#     response = await client.post(
#         "/auth/register",
#         json={
#             "first_name": "test_firstname",
#             "middle_name": "test_middlename",
#             "last_name": "test_lastname",
#             "email": "test@example.com",
#             "password": "password123",
#             "due_date": "2026-05-10",
#         },
#     )
#     assert response.status_code == status.HTTP_201_CREATED


# @pytest.mark.asyncio
# async def test_register_excluded_middle_name_success(client: AsyncClient) -> None:
#     response = await client.post(
#         "/auth/register",
#         json={
#             "first_name": "test_firstname",
#             "last_name": "test_lastname",
#             "email": "test@example.com",
#             "password": "password123",
#             "due_date": "2026-05-10",
#         },
#     )
#     assert response.status_code == status.HTTP_201_CREATED


# @pytest.mark.asyncio
# async def test_register_conflict(client: AsyncClient) -> None:
#     conflicting_email: str = "test@example.com"

#     await client.post(
#         "/auth/register",
#         json={
#             "first_name": "user1_firstname",
#             "last_name": "user1_lastname",
#             "email": conflicting_email,
#             "password": "password123",
#             "due_date": "2026-05-10",
#         },
#     )

#     response = await client.post(
#         "/auth/register",
#         json={
#             "first_name": "user2_firstname",
#             "last_name": "user2_lastname",
#             "email": conflicting_email,
#             "password": "password123",
#             "due_date": "2026-05-10",
#         },
#     )
#     assert response.status_code == status.HTTP_409_CONFLICT, "Expected 409 CONFLICT for duplicate email registration"
