import discord

from discord.ext import commands
from src.commands.helpers import timestamp


class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    async def clear(self, ctx, number):
        clear = int(number)
        username = ctx.author.mention
        channel = self.bot.get_channel(819217765188501536)
        if ctx.author.guild_permissions.ban_members:
            clearedmessages = discord.Embed(color=0x00FF00)
            clearedmessages.add_field(
                name="Cleared Messages",
                value=f"{username}has cleared {clear} messages.",
            )
            await ctx.channel.purge(limit=clear)
            await ctx.channel.send(f"I have cleared {number} messages.")

            await channel.send(timestamp, embed=clearedmessages)
        else:
            await ctx.channel.send(
                "You don't have the correct permissions to clear messages."
            )

    @commands.command(name="ban")
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        if ctx.author.guild_permissions.ban_members:
            ban = discord.Embed(
                title=f":hammer:Successfully banned {user}",
                description=f"Reason: {reason}\nBy: {ctx.author.mention}",
            )
            channel = self.bot.get_channel(755522585864962099)
            await user.ban(reason=reason)
            await ctx.channel.send(embed=ban)

            await channel.send(embed=ban)
        else:
            await ctx.channel.send("You don't have the correct permissions.")

    @commands.command(name="unban")
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        if ctx.author.guild_permissions.ban_members:
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (
                    member_name,
                    member_discriminator,
                ):
                    unban = discord.Embed(
                        title=f"Successfully Unbanned {user}",
                        description=f"By: {ctx.author.mention}",
                    )
                    channel = self.bot.get_channel(819217765188501536)
                    await ctx.guild.unban(user)
                    await ctx.channel.send(embed=unban)

                    await channel.send(embed=unban)
        else:
            await ctx.channel.send("You don't have the correct permissions.")

    @commands.command(name="kick")
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        if ctx.author.guild_permissions.ban_members:
            kick = discord.Embed(
                title=f":hammer:Successfully kicked {user}",
                description=f"Reason: {reason}\nBy: {ctx.author.mention}",
            )
            channel = self.bot.get_channel(819217765188501536)
            await user.kick(reason=reason)
            await ctx.channel.send(embed=kick)

            await channel.send(embed=kick)
        else:
            await ctx.channel.send("You don't have the correct permissions.")


def setup(bot):
    bot.add_cog(Mods(bot))
