from typing import List, Dict

class EconomyService:
    def __init__(self, db):
        self.db = db

    async def get_top_balances(self, limit: int = 10) -> List[Dict]:
        return await self.db.get_top_users(limit)

    async def add_money(self, user_id: int, amount: int) -> bool:
        return await self.db.add_money(user_id, amount)