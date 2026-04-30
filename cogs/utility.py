from discord.ext import commands
import discord

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="ping", description="Check if the bot is responsive")
    async def ping(self, ctx):
        latency = self.bot.latency * 1000
        await ctx.send(f"Latency: {latency:.2f}")
    
    @commands.hybrid_command(name="cmds", description="Get a list of commands")
    async def cmds(self, ctx):
        embed = discord.Embed(
            title="Nova Commands",
            color=0x7ba3b0
        )
        embed.add_field(name="!ping", value="Get latency of the bot", inline=False)
        embed.add_field(name="!cmds", value="Get commands of the bot", inline=False)
        embed.add_field(name="!setup", value="Helps you to setup Nova for your server!", inline=False)
        embed.add_field(name="!weather <city>", value="Get weather of a specified city", inline=False)
        embed.add_field(name="!kick <member> <reason>", value="Kicks a member", inline=False)
        embed.add_field(name="!ban <member> <reason>", value="Bans a member", inline=False)
        embed.add_field(name="!timeout <member> <duration>", value="A member is timedout for specific duration")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))