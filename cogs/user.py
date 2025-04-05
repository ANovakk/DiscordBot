import discord
from discord.ext import commands
from services.paginator import Paginator

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service
        self.economy_service = bot.economy_service
        self.logger = bot.logger

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.mention}!')

    @commands.command()
    async def register(self, ctx):
        """Register a new user command."""

        status = await self.user_service.register_user(ctx.author)

        messages = {
            "created": "✅ Registration successful!",
            "exists": "ℹ️ You are already registered",
            "error": "❌ Registration error"
        }

        await ctx.send(messages[status])

    @commands.command(name='top')
    async def get_top_users(self, ctx):
        """Get the top 10 users by Balance, by Discord Activity"""

        self.logger.info("Getting top users")

        top_users_by_activity = await self.user_service.get_top_users_by_activity()
        top_users_by_balance = await self.economy_service.get_top_users_by_balance()

        page1 = discord.Embed(
            title="Top Users by time in voice channels",
            description="\n".join(f"{i + 1}. {user}" for i, user in enumerate(top_users_by_activity)),
            color=0x3498db
        )

        page2 = discord.Embed(
            title="Top Users by Balance",
            description="\n".join(f"{i + 1}. {user}" for i, user in enumerate(top_users_by_balance)),
            color=0x2ecc71
        )

        pages = [page1, page2]
        view = Paginator(pages)
        await ctx.send(embed=pages[0], view=view)



async def setup(bot):
    await bot.add_cog(UserCog(bot))