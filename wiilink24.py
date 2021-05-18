import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

bot.load_extension("src.commands.misc")
bot.load_extension("src.commands.mod")
bot.load_extension("src.commands.events")
bot.load_extension("src.commands.converters")



bot.run(TOKEN)


