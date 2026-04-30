import discord
from dotenv import load_dotenv
from discord.ext import commands
import os

load_dotenv(".env")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN") 

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    for file in os.listdir("cogs"):
        if file.startswith("__") or not file.endswith(".py"):
            continue
        await bot.load_extension(f"cogs.{file[:-3]}")
    await bot.start(DISCORD_TOKEN)
@bot.event
async def on_ready():
    print(f"{bot.user} has connected!")

@bot.event
async def on_member_join(member: discord.Member):
    try:
        channel = discord.utils.get(member.guild.text_channels, name="joins")
        await channel.send(f"{member.mention} has arrived!")
    except Exception as e:
        print(f"{e}")
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())