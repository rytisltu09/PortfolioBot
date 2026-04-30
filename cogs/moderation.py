import datetime
import discord
from discord.ext import commands

LOG_CHANNEL_NAME = "nova-logs"


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild: discord.Guild):
        return discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)

    @commands.hybrid_command(name="kick", description="Kick a member from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            channel = await self.get_log_channel(ctx.guild)
            if channel:
                embed = discord.Embed(
                    title="Member Kicked",
                    color=0xFEE75C,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)

                await channel.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Failed to kick {member}. Error: {e}")

    @commands.hybrid_command(name="ban", description="Ban a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member} has been kicked from the server. Reason: {reason}")

            channel = await self.get_log_channel(ctx.guild)
            if channel:
                embed = discord.Embed(
                    title="Member Banned",
                    color=0xED4245,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)

                await channel.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Failed to ban {member}. Error: {e}")

    @commands.hybrid_command(name="timeout", description="Timeout a member for a specified duration.")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: int, *, reason=None):
        try:
            timeout_until = discord.utils.utcnow() + datetime.timedelta(minutes=duration)
            await member.timeout(timeout_until, reason=reason)
            await ctx.send(f"{member.mention} has been muted for {duration} minutes.")

            channel = await self.get_log_channel(ctx.guild)
            if channel:
                embed = discord.Embed(
                    title="Member Timed Out",
                    color=0x5865F2,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Duration", value=f"{duration} minutes", inline=False)
                embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)

                await channel.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Failed to timeout {member}. Error: {e}")


async def setup(bot):
    await bot.add_cog(Moderation(bot))