import discord
from discord.ext import commands
from database.databaseManager import DatabaseManager
from services.economyService import EconomyService
import os
from dotenv import load_dotenv
from logger.logger import setup_logging

from services.userService import UserService

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix='!', intents=intents)

        # Logger
        self.logger = setup_logging()

        # DataBase
        self.db = DatabaseManager(self.logger)

        # Services
        self.economy_service = EconomyService(self.db, self.logger)
        self.user_service = UserService(self.db, self.logger)


    async def setup_hook(self):
        await self.init_db()
        await self.load_cogs()

    async def init_db(self):
        try:
            await self.db.connect()
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            await self.close()

    async def load_cogs(self):
        try:
            await self.load_extension('cogs.economy')
            await self.load_extension('cogs.server_events')
            await self.load_extension('cogs.user')

            self.logger.info("Cogs were loaded successfully")
        except commands.ExtensionError as e:
            self.logger.error(f"Cog loading error: {e}")

    async def close(self):
        await self.db.close()
        await super().close()

bot = MyBot()

@bot.event
async def on_ready():
    bot.logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')

if __name__ == '__main__':
    try:
        bot.run(os.getenv('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        bot.logger.info("\nBot stopped by user")