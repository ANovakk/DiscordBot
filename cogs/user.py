from discord.ext import commands

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

        top_users_by_activity = await self.user_service.get_top_users_by_activity(ctx)
        top_users_by_balance = await self.economy_service.get_top_users_by_balance(ctx)

async def setup(bot):
    await bot.add_cog(UserCog(bot))