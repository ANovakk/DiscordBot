from discord.ext import commands

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = bot.economy_service

    @commands.command(name="top")
    async def show_top(self, ctx):
        await ctx.send("Top ten users")

    @commands.command(name="get")
    async def get_money(self, ctx):
        result = await self.economy.add_money(ctx.author.id, 1000)


async def setup(bot):
    await bot.add_cog(EconomyCog(bot))