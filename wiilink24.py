import os
import random
import discord
import asyncio
import src.commands


from dotenv import load_dotenv
from typing import Optional
from discord.ext import commands
from discord import Embed, Member, NotFound, Object
from datetime import datetime, timedelta
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, has_role

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='/')


@bot.command(name='clear', help='this command will clear msgs')
@commands.has_role('Owner')
async def clear(ctx, number):
	clear = int(number)
	await ctx.channel.purge(limit=clear)
	await ctx.send(f'I have cleared {number} messages.')



#The below code bans player.
@bot.command(name='ban')
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)



#The below code unbans player.
@bot.command(name='unban')
@commands.has_role('Owner')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name) == (member_name):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


bot.run(TOKEN)