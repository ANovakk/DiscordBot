from discord.ext import commands

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

async def setup(bot):
    await bot.add_cog(ServerEvents(bot))
