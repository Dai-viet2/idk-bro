import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from view import setup_view
from claim import setup_claim

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

setup_view(bot)
setup_claim(bot)

bot.run(TOKEN)
