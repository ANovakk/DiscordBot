import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self, logger):
        self.logger = logger
        self.pool = None
        self.connection_url = os.getenv('DATABASE_URL')

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            self.connection_url,
            statement_cache_size=0)
        self.logger.info("Database connection established")

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.logger.info("Connection with database is closed")

    """
    Functions to work with Users
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
    Functions to work with Money
    """

    async def add_money(self, user_id, amount) -> bool:
        result = await self.pool.execute(
            "UPDATE users "
            "SET balance = balance + $1 "
            "WHERE id = $2",
            amount, str(user_id)
        )
        return result

    """
    Functions to work with Voice channel records
    """

    async def change_last_join_time(self, user_id, time):
        self.logger.info(f"Change last join time {user_id} {time}")
        try:
            await self.pool.execute(
                "UPDATE users "
                "SET last_join_time = $1 "
                "WHERE user_id = $2",
                time, str(user_id)
            )
        except Exception as e:
            self.logger.error(e)

    async def get_last_join_time(self, user_id) -> str:
        self.logger.info(f"Get last join time {user_id}")
        try:
            last_join_time = await self.pool.fetchval(
               "SELECT last_join_time FROM users "
                "WHERE user_id = $1",
                str(user_id)
            )
            return last_join_time
        except Exception as e:
            self.logger.error(e)

    async def add_total_voice_time(self, user_id, time):
        self.logger.info(f"Add total voice time {user_id} {time}")
        try:
            await self.pool.execute(
                "UPDATE users "
                "SET total_voice_time = total_voice_time + $1 "
                "WHERE user_id = $2",
                time, str(user_id)
            )
        except Exception as e:
            self.logger.error(e)

    async def add_voice_channel_log(self, user_id, channel_id,
                                        channel_name, join_time,
                                        leave_time, duration):
        self.logger.info(f"Add voice channel log {user_id} {channel_name} {duration} seconds")
        try:
            await self.pool.execute(
                "INSERT INTO voice_logs"
                "(user_id, channel_id, channel_name, join_time, leave_time, duration)"
                "VALUES ($1, $2, $3, $4, $5, $6)",
                str(user_id), str(channel_id), channel_name,
                 join_time, leave_time, duration
            )
        except Exception as e:
            self.logger.error(e)