import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp

load_dotenv(".env")
API_KEY = os.getenv("WEATHER_API_KEY")

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="weather", description="Get weather information from a specified city")
    async def weather(self, ctx, *, city: str):
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
            if "error" in data:
                await ctx.send("❌ City not found.")
                return

            location = data["location"]
            current = data["current"]

            embed = discord.Embed(
                title=f"🌤 Weather in {location['name']}, {location['country']}",
                color=discord.Color.blue()
            )

            icon_url = self.bot.user.display_avatar.url

            embed.set_author(name="NovaAPP", icon_url=icon_url)
            embed.add_field(name="Temperature", value=f"{current['temp_c']}°C", inline=True)
            embed.add_field(name="Feels Like", value=f"{current['feelslike_c']}°C", inline=True)
            embed.add_field(name="Humidity", value=f"{current['humidity']}%", inline=True)
            embed.add_field(name="Wind", value=f"{current['wind_kph']} km/h", inline=True)
            embed.add_field(name="Pressure", value=f"{current["pressure_mb"]} mb")
            embed.add_field(name="Condition", value=f"{current["condition"]["text"]}", inline=True)
            embed.add_field(name="Disclaimer:", value="Given data can have minor inaccuracies.", inline=False)
            embed.set_thumbnail(url="https:" + current["condition"]["icon"])
            embed.set_footer(text="Powered by WeatherAPI")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("❌ Failed to fetch weather.")
            print(e)

async def setup(bot):
    await bot.add_cog(Weather(bot))
