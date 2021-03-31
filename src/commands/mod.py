import discord
import os
import psycopg2

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.commands.utils import connection, generate_random
import src.commands
import sqlalchemy
import config

engine = create_engine(config.db_url, echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

fmt = "%a, %d %b %Y | %H:%M:%S %ZGMT"


# Database structure only exists
# So Python doesn't return a undefined error
class strike(Base):
    __tablename__ = 'strike'

    userid = Column(Integer, primary_key=True)
    strikes = Column(Integer)
    reason = Column(String)


@bot.command(name='clear')
async def clear(ctx, number):
    clear = int(number)
    username = ctx.author.mention
    channel = bot.get_channel(819217765188501536)
    if ctx.author.guild_permissions.ban_members:
        timestamp = datetime.utcnow().strftime('`%H:%M:%S`')
        clearedmessages = discord.Embed(color=0x00ff00)
        clearedmessages.add_field(name='Cleared Messages', value=f'{username}has cleared {clear} messages.')
        await ctx.channel.purge(limit=clear)
        await ctx.channel.send(f'I have cleared {number} messages.')

        await channel.send(timestamp, embed=clearedmessages)
    else:
        await ctx.channel.send("You don't have the correct permissions to clear messages.")


@bot.command(name='about')
async def about(message):
    text = "<:AkkoWink:819398419289210880> About WiiLink24 Bot"
    embed = discord.Embed(color=0x00ff00)
    embed.set_thumbnail(url=message.guild.icon_url)
    embed.add_field(name="Created By:", value='SketchMaster2001')
    embed.add_field(name="Created For:", value='WiiLink24 under the GPL-3.0 License', inline=False)
    embed.add_field(name="More Info",
                    value='It is always broken, is no longer broken.\nPrefix is `/`. This is currently being hosted on my PC so please go easy on the commands.\nWritten in python because JS sucks.',
                    inline=False)
    await message.channel.send(text, embed=embed)


@bot.command(name='strike')
async def strik(ctx, user: discord.Member, number, *, reason):
    if ctx.author.guild_permissions.ban_members:
        bruv = await user.create_dm()
        strikemsg = discord.Embed(title=f":hammer:Successfully striked {user}",
                               description=f"Reason: {reason}\nNumber of Strikes: {number}\nBy: {ctx.author.mention}")
        channel = bot.get_channel(819217765188501536)

        db_strikes = [strike(userid=user.id, strikes=number, reason=reason)]
        session.bulk_save_objects(db_strikes)
        session.commit()

        await ctx.channel.send(embed=strikemsg)

        await bruv.send(f"<:warn:821441284233363487> You have been given `{number}` strikes in WiiLink24 for: `{reason}`.")

        # Auto Punishments
        cursor = connection.cursor()
        grab_id = """select * from strike where userid = %s"""
        cursor.execute(grab_id, (user.id,))
        records = cursor.fetchall()

        for row in records:
            strikes = row[1]

        if strikes == 4:
            await user.kick(reason=reason)
    else:
        await ctx.channel.send("You don't have the correct permissions.")


@bot.command(name='check')
async def check(ctx, user: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        userid = user.id
        cursor = connection.cursor()
        grab_id = """select * from strike where userid = %s"""
        cursor.execute(grab_id, (userid,))
        records = cursor.fetchall()

        for row in records:
            users = "User ID: ", row[0]
            strikes = row[1]

        embed = discord.Embed(title=f"About {user}", color=0x00ff00)
        embed.add_field(name=f"Strikes:", value=f"{strikes}")
        await ctx.channel.send(embed=embed)


@bot.command(name='ban')
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
    if ctx.author.guild_permissions.ban_members:
        ban = discord.Embed(title=f":hammer:Successfully banned {user}",
                            description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        channel = bot.get_channel(819217765188501536)
        await user.ban(reason=reason)
        await ctx.channel.send(embed=ban)

        await channel.send(embed=ban)
    else:
        await ctx.channel.send("You don't have the correct permissions.")


@bot.command(name='unban')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    if ctx.author.guild_permissions.ban_members:
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                unban = discord.Embed(title=f"Successfully Unbanned {user}", description=f"By: {ctx.author.mention}")
                channel = bot.get_channel(819217765188501536)
                await ctx.guild.unban(user)
                await ctx.channel.send(embed=unban)

                await channel.send(embed=unban)
    else:
        await ctx.channel.send("You don't have the correct permissions.")


@bot.command(name='apply')
async def apps(ctx, *, username: discord.Member = None):
    if username is None:
        username = ctx.author
    user = username.id
    bruv = await username.create_dm()
    user = username.id
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="To Apply:", value="Go to your DM's and click the link provided by WiiLink24 Bot.")
    await ctx.channel.send(embed=embed)
    await bruv.send(f"Click the link below to apply for mod!\nhttps://tripetto.app/run/849CLXP5VM?userid={user}")


@bot.command(name='kick')
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    if ctx.author.guild_permissions.ban_members:
        kick = discord.Embed(title=f":hammer:Successfully kicked {user}",
                             description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        channel = bot.get_channel(819217765188501536)
        await user.kick(reason=reason)
        await ctx.channel.send(embed=kick)

        await channel.send(embed=kick)
    else:
        await ctx.channel.send("You don't have the correct permissions.")


@bot.command(name='avy', aliases=["avatar"])
async def avatar(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    embed = discord.Embed(color=0x00ff00)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_image(url=user.avatar_url)
    await ctx.channel.send(embed=embed)


@bot.command(name='riitag', aliases=["tag"])
async def riitag(ctx, *, username: discord.Member = None):
    if username is None:
        username = ctx.author
    randomizer = generate_random(6)
    user = username.id
    em = discord.Embed(color=0x00ff00)
    em.set_author(name=f"{username}'s RiiTag", icon_url=username.avatar_url)
    em.set_image(url=f"https://tag.rc24.xyz/{user}/tag.max.png?randomizer=0.{randomizer}")
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
        embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    await ctx.send(embed=embed)


# Service Stats
@bot.command(name='stats')
async def stats(message):
    embedVar = discord.Embed(title="<:wiilink24:818538825948987512> WiiLink24 Service Stats", color=0x00ff00)
    embedVar.add_field(name="Public Beta:", value='```yaml\n+ Wii no Ma```\n+ Wii Fit Body Check Channel', inline=False)
    embedVar.add_field(name="Private Beta:", value='```fix\n* Digicam Print Channel```', inline=False)
    embedVar.add_field(name="In Development", value='```fix\n*Demae Channel```', inline=False)
    embedVar.add_field(name="Not in Development:",
                       value='```diff\n- Dokodemo Wii no Ma\n- TV no Tomo Channel G Guide for Wii```', inline=False)
    await message.channel.send(embed=embedVar)


@bot.command(name='serverinfo')
async def on_message(message):
    title = f"<:info:818678491528036366> Information About **{message.guild.name}**:"
    embed = discord.Embed(color=0x00ff00)
    text_channels = len(message.guild.text_channels)
    voice_channels = len(message.guild.voice_channels)
    categories = len(message.guild.categories)
    channels = text_channels + voice_channels
    embed.set_thumbnail(url=str(message.guild.icon_url))
    embed.add_field(name=f"**{message.guild.name}**",
                    value=f":white_small_square: ID: **{message.guild.id}** \n:white_small_square: Owner: **{message.guild.owner}** \n:white_small_square: Location: **{message.guild.region}** \n:white_small_square: Creation: **{message.guild.created_at.strftime(fmt)}** \n:white_small_square: Members: **{message.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(message.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in message.guild.features)}")
    embed.set_image(url=f"https://cdn.discordapp.com/splashes/750581992223146074/{message.guild.splash}.jpg")
    await message.channel.send(title, embed=embed)


bot.run(TOKEN)
