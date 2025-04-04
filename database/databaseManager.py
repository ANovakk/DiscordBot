import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.connection_url = os.getenv('DATABASE_URL')

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            self.connection_url,
            statement_cache_size=0)
        print("Connection with database is established")

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("Connection with database is closed")


    """
    Commands to work with Users
    """

    async def register_user(self, member) -> str:
        try:
            async with self.pool.acquire() as conn:
                user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", str(member.id))

                if user:
                    return "exists"

                await conn.execute("""
                    INSERT INTO users (user_id, username, balance)
                    VALUES ($1, $2, $3)
                """, str(member.id), str(member.name), 100000)

                return "created"

        except Exception as e:
            print(f"[register_user] Ошибка: {e}")
            return "error"

    async def get_top_users(self, limit: int = 10) -> list[dict]:
        """
        Function to get top users by balance
        """
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                "SELECT id, balance FROM users "
                "ORDER BY balance DESC LIMIT $1",
                limit
            )
            return [dict(record) for record in records]

    """
    Commands to work with Money
    """

    async def add_money(self, user_id: int, amount: int) -> bool:
        result = await self.pool.execute(
            "UPDATE users "
            "SET balance = balance + $1 "
            "WHERE id = $2", (amount, user_id)
        )
        return result