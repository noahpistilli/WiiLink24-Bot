import discord
import os

from discord.ext.commands import command
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

@bot.command(name='avy', aliases=["avatar"])
async def avatar(ctx, *, user: discord.Member = None):
	if user is None:
    		user = ctx.author  
	embed = discord.Embed(color=0x00ff00)
	embed.set_author(name=str(user), icon_url=user.avatar_url)
	embed.set_image(url=user.avatar_url)
	await ctx.channel.send(embed=embed)


@bot.command(name='riitag', aliases=["tag"])  
async def on_message(ctx, *, username: discord.Member = None):
	if username is None:
    		username = ctx.author
	user = username.id
	em = discord.Embed(color=0x00ff00)
	em.set_author(name=f"{username}'s RiiTag", icon_url=username.avatar_url)
	em.set_image(url=f"https://tag.rc24.xyz/{user}/tag.max.png")
	await ctx.channel.send(embed=em)


@bot.command(name='userinfo')
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0x00ff00, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)


# Service Stats
@bot.command(name='stats')
async def on_message(message):
        embedVar = discord.Embed(title="<:wiilink24:818538825948987512> WiiLink24 Service Stats", color=0x00ff00)
        embedVar.add_field(name="Public Beta:", value='```yaml\n+ Wii no Ma```', inline=False)
        embedVar.add_field(name="Private Beta:", value='```fix\n* Digicam Print Channel\n* Demae Channel```', inline=False)
        embedVar.add_field(name="Not in Development:", value='```diff\n- Dokodemo Wii no Ma\n- TV no Tomo Channel G Guide for Wii```', inline=False)
        await message.channel.send(embed=embedVar)


@bot.command(name='serverinfo')  
async def on_message(message):
       embed = discord.Embed(title=f"<:info:818678491528036366> Information About **{message.guild.name}**:", color=0x00ff00)
       text_channels = len(message.guild.text_channels)
       voice_channels = len(message.guild.voice_channels)
       categories = len(message.guild.categories)
       channels = text_channels + voice_channels
       embed.set_thumbnail(url = str(message.guild.icon_url))
       embed.add_field(name = f"**{message.guild.name}**", value = f":white_small_square: ID: **{message.guild.id}** \n:white_small_square: Owner: **{message.guild.owner}** \n:white_small_square: Location: **{message.guild.region}** \n:white_small_square: Creation: **{message.guild.created_at.strftime(format)}** \n:white_small_square: Members: **{message.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(message.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in message.guild.features)} \n:white_small_square: Splash: {message.guild.splash}")
       await message.channel.send(embed=embed)


bot.run(TOKEN)

