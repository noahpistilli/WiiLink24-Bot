import os
import discord

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

bot.load_extension("src.commands.misc")
bot.load_extension("src.commands.mod")

bot.run(TOKEN)
