import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import webserver

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a bot!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

webserver.keep_alive()
bot.run(token)
