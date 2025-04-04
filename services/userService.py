class UserService:
    def __init__(self, db):
        self.db = db

    async def register_user(self, member):
        """
        Registers a Discord member in the database.
        Returns 'created' on success, 'exists' if already registered, or 'error' on failure.
        """

        result = await self.db.register_user(member)

        if result == "created":
            print(f"User {member.name} registered successfully")
        elif result == "exists":
            print(f"User {member.name} is already registered")
        else:
            print(f"Error registering user {member.name}")

        return result