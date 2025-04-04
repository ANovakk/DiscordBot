from discord.ext import commands

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_service = bot.user_service

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

async def setup(bot):
    await bot.add_cog(UserCog(bot))