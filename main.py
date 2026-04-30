from database import add_favorite_city, get_favorite_city, remove_favorite_city
import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.hybrid_command(name='ping', description='Check if the bot is responsive')
async def ping(ctx):
    embed = discord.Embed(
        title='🏓 Pong!',
        description='The bot is responsive and ready to provide weather updates!',
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name='weather', description='Get the current weather for a city')
async def weather(ctx, *, city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        icon = data['weather'][0]['icon']
        icon_url = f'http://openweathermap.org/img/wn/{icon}@2x.png'
        
        embed = discord.Embed(
            title=f'🌤️ Weather in {city.title()}',
            color=0x3498db
        )
        embed.add_field(name='Temperature', value=f'{temp}°C', inline=True)
        embed.add_field(name='Feels Like', value=f'{feels_like}°C', inline=True)
        embed.add_field(name='Condition', value=description.capitalize(), inline=True)
        embed.add_field(name='Humidity', value=f'{humidity}%', inline=True)
        embed.add_field(name='Wind Speed', value=f'{wind_speed} m/s', inline=True)
        embed.set_thumbnail(url=icon_url)
        embed.set_footer(text='Powered by OpenWeatherMap')
        
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='❌ Error',
            description=f'Could not retrieve weather data for {city}. Please check the city name.',
            color=0xff0000
        )
        await ctx.send(embed=embed)

@bot.hybrid_command(name='favorite', description='Set or get your favorite city for weather updates')
async def favorite(ctx, *, city: str = None):
    user_id = ctx.author.id
    if city:
        add_favorite_city(user_id, city)
        embed = discord.Embed(
            title='✅ Favorite City Set',
            description=f'Your favorite city has been set to **{city.title()}**.',
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    else:
        favorite_city = get_favorite_city(user_id)
        if favorite_city:
            embed = discord.Embed(
                title='⭐ Your Favorite City',
                description=f'Your favorite city is **{favorite_city.title()}**.',
                color=0xffd700
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='❓ No Favorite City',
                description='You have not set a favorite city yet. Use `!favorite <city>` to set one.',
                color=0xffa500
            )
            await ctx.send(embed=embed)

@bot.hybrid_command(name='unfavorite', description='Remove your favorite city')
async def unfavorite(ctx):
    user_id = ctx.author.id
    favorite_city = get_favorite_city(user_id)
    if favorite_city:
        remove_favorite_city(user_id)
        embed = discord.Embed(
            title='🗑️ Favorite City Removed',
            description=f'Your favorite city **{favorite_city.title()}** has been removed.',
            color=0xff4500
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='❓ No Favorite City',
            description='You have no favorite city to remove.',
            color=0xffa500
        )
        await ctx.send(embed=embed)

@bot.hybrid_command(name='myweather', description='Get the weather for your favorite city')
async def myweather(ctx):
    user_id = ctx.author.id
    favorite_city = get_favorite_city(user_id)
    if favorite_city:
        await weather(ctx, city=favorite_city)
    else:
        embed = discord.Embed(
            title='❓ No Favorite City',
            description='You have not set a favorite city yet. Use `!favorite <city>` to set one.',
            color=0xffa500
        )
        await ctx.send(embed=embed)

@bot.hybrid_command(name='commands', description='Show this help message')
async def help_command(ctx):
    embed = discord.Embed(
        title='📖 Weather Bot Commands',
        description='Here are the available commands:',
        color=0x1abc9c
    )
    embed.add_field(name='!ping', value='Check if the bot is responsive', inline=False)
    embed.add_field(name='!weather <city>', value='Get the current weather for a city', inline=False)
    embed.add_field(name='!favorite <city>', value='Set your favorite city for weather updates', inline=False)
    embed.add_field(name='!favorite', value='Get your currently set favorite city', inline=False)
    embed.add_field(name='!unfavorite', value='Remove your favorite city', inline=False)
    embed.add_field(name='!myweather', value='Get the weather for your favorite city', inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)