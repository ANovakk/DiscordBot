from typing import List, Dict

class UserService:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    async def register_user(self, member):
        """
        Registers a Discord member in the database.
        Returns 'created' on success, 'exists' if already registered, or 'error' on failure.
        """

        result = await self.db.register_user(member)

        if result == "created":
            self.logger.info(f"User {member.name} registered successfully")
        elif result == "exists":
            self.logger.info(f"User {member.name} is already registered")
        else:
            self.logger.error(f"Error registering user {member.name}")

        return result

    async def get_top_users_by_activity(self, limit: int = 10) -> List[Dict]:
        return await self.db.get_top_users_by_balance(limit)