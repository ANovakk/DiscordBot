from discord.ext import commands

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = bot.economy_service

    @commands.command(name="get")
    async def get_money(self, ctx):
        result = await self.economy.add_money(ctx.author.id, 1000)

    @commands.command(name="balance")
    async def balance_funds(self, ctx):
        pass

    @commands.command(name="transfer")
    async def transfer_funds(self, ctx, from_id, to_id, amount):
        pass

    @commands.command(name="deposit")
    async def deposit_funds(self, ctx, amount):
        pass

    @commands.command(name="withdraw")
    async def withdraw_funds(self, ctx, amount):
        pass

    @commands.command(name="earn")
    async def earn_funds(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(EconomyCog(bot))