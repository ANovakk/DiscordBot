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

    async def voice_record(self, user_id, channel_id, channel_name, time, flag):
        """

        :param user_id:
        :param time: Time when event was recorded.
        :param flag: Join the voice channel: 0
                     Leave the voice channel: 1
                     Change the voice channel: 2
        :return:
        """

        if flag == 0:
            await self.db.change_last_join_time(user_id, time)
        elif flag == 1:
            time_from = await self.db.get_last_join_time(user_id)
            duration = int((time - time_from).total_seconds())

            await self.db.add_voice_channel_log(user_id, channel_id, channel_name, time_from, time, duration)
            await self.db.add_total_voice_time(user_id, duration)