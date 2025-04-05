from discord.ext import commands
from datetime import datetime

class ServerEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service
        self.logger = bot.logger

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.logger.info(f"Bot joined the server: {guild.name}")
        async for member in guild.fetch_members(limit=None):
            await self.user_service.register_user(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.logger.info(f"{member.name} joined the server {member.guild.name}")
        await self.user_service.register_user(member)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            time = datetime.now()
            if before.channel is None and after.channel is not None and not after.afk:
                self.logger.info(f"{member.name} joined the voice channel")
                await self.user_service.voice_record(member.id, after.channel.id, after.channel.name, time, 0)

            elif before.channel is not None and after.channel is None and not before.afk:
                self.logger.info(f"{member.name} left the voice channel")
                await self.user_service.voice_record(member.id, before.channel.id, before.channel.name, time, 1)

            elif before.channel is not None and after.channel is not None:
                if before.afk and not after.afk:
                    self.logger.info(f"{member.name} left AFK and joined the voice channel")
                    await self.user_service.voice_record(member.id, after.channel.id, after.channel.name, time, 0)

                elif not before.afk and after.afk:
                    self.logger.info(f"{member.name} left the voice channel and went AFK")
                    await self.user_service.voice_record(member.id, before.channel.id, before.channel.name, time, 1)

                elif not before.afk and not after.afk:
                    self.logger.info(f"{member.name} changed the voice channel")
                    await self.user_service.voice_record(member.id, before.channel.id, before.channel.name, time, 1)
                    await self.user_service.voice_record(member.id, after.channel.id, after.channel.name, time, 0)

        except Exception as e:
            self.logger.error(e)

async def setup(bot):
    await bot.add_cog(ServerEvents(bot))
