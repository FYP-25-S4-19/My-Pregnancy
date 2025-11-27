from sqlalchemy.ext.asyncio import AsyncSession


class AccountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # def submit_account_creation_request(self, )
