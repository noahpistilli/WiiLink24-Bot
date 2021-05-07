import discord

from discord.ext import commands
from src.commands.helpers import generate_random

fmt = "%a, %d %b %Y | %H:%M:%S %ZGMT"


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def about(self, message):
        text = "<:AkkoWink:819398419289210880> About WiiLink24 Bot"
        embed = discord.Embed(color=0x00FF00)
        embed.set_thumbnail(url=message.guild.icon_url)
        embed.add_field(name="Created By:", value="SketchMaster2001")
        embed.add_field(
            name="Created For:",
            value="WiiLink24 under the GPL-3.0 License",
            inline=False,
        )
        embed.add_field(
            name="More Info",
            value="It is always broken, is no longer broken.\nPrefix is `/`. This is currently being hosted on my PC so please go easy on the commands.\nWritten in python because JS sucks.",
            inline=False,
        )
        await message.channel.send(text, embed=embed)

    @commands.command(name="avy", aliases=["avatar"])
    async def avatar(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(color=0x00FF00)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_image(url=user.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.command(name="riitag", aliases=["tag"])
    async def riitag(self, ctx, *, username: discord.Member = None):
        if username is None:
            username = ctx.author
        randomizer = generate_random(6)
        user = username.id
        em = discord.Embed(color=0x00FF00)
        em.set_author(name=f"{username}'s RiiTag", icon_url=username.avatar_url)
        em.set_image(
            url=f"https://tag.rc24.xyz/{user}/tag.max.png?randomizer=0.{randomizer}"
        )
        await ctx.channel.send(embed=em)

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0x00FF00, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_string = ", ".join(
            [
                str(p[0]).replace("_", " ").title()
                for p in user.guild_permissions
                if p[1]
            ]
        )
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text="ID: " + str(user.id))
        await ctx.send(embed=embed)

    # Service Stats
    @commands.command(pass_context=True)
    async def stats(self, message):
        embedVar = discord.Embed(
            title="<:wiilink24:818538825948987512> WiiLink24 Service Stats",
            color=0x00FF00,
        )
        embedVar.add_field(
            name="Public Beta:", value="```yaml\n+ Wii no Ma```", inline=False
        )
        embedVar.add_field(
            name="Private Beta:",
            value="```fix\n* Digicam Print Channel\n* Demae Channel```",
            inline=False,
        )
        embedVar.add_field(
            name="Private Beta:",
            value="```fix\n* Wii Fit Body Check Channel```",
            inline=False,
        )
        embedVar.add_field(
            name="Not in Development:",
            value="```diff\n- Dokodemo Wii no Ma\n- TV no Tomo Channel G Guide for Wii```",
            inline=False,
        )
        await message.channel.send(embed=embedVar)

    @commands.command(name="serverinfo")
    async def server_info(self, message):
        title = (
            f"<:info:818678491528036366> Information About **{message.guild.name}**:"
        )
        embed = discord.Embed(color=0x00FF00)
        text_channels = len(message.guild.text_channels)
        voice_channels = len(message.guild.voice_channels)
        categories = len(message.guild.categories)
        channels = text_channels + voice_channels
        embed.set_thumbnail(url=str(message.guild.icon_url))
        embed.add_field(
            name=f"**{message.guild.name}**",
            value=f":white_small_square: ID: **{message.guild.id}** \n:white_small_square: Owner: **{message.guild.owner}** \n:white_small_square: Location: **{message.guild.region}** \n:white_small_square: Creation: **{message.guild.created_at.strftime(fmt)}** \n:white_small_square: Members: **{message.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(message.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in message.guild.features)}",
        )
        embed.set_image(
            url=f"https://cdn.discordapp.com/splashes/750581992223146074/{message.guild.splash}.jpg"
        )
        await message.channel.send(title, embed=embed)

    @commands.command()
    async def hex_to_str(self, ctx, hex):
        no_whitespace = hex.replace(" ", "")

        de_hex = bytearray.fromhex(no_whitespace).decode()

        await ctx.channel.send(de_hex)


def setup(bot):
    bot.add_cog(Misc(bot))


###################################################################################################################
# @bot.command(name='apply')                                                                                      #
# async def apps(ctx, *, username: discord.Member = None):                                                        #
#    if username is None:                                                                                         #
#        username = ctx.author                                                                                    #
#   user = username.id                                                                                            #
#    bruv = await username.create_dm()                                                                            #
#    user = username.id                                                                                           #
#    embed = discord.Embed(color=0x00ff00)                                                                        #
#    embed.add_field(name="To Apply:", value="Go to your DM's and click the link provided by WiiLink24 Bot.")     #
#    await ctx.channel.send(embed=embed)                                                                          #
#    await bruv.send(f"Click the link below to apply for mod!\nhttps://tripetto.app/run/849CLXP5VM?userid={user}")#
###################################################################################################################
