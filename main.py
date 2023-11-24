import discord, os, asyncio
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, application_id='991731064026448043')

@bot.event
async def on_ready():
    print(f"Ready for action! Logged in as {bot.user}")

@bot.command
async def sync(ctx):
    fmt = await ctx.bot.tree.sync(guild = ctx.guild)
    await ctx.send(f"Refreshed {len(fmt)} commands.")


async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())