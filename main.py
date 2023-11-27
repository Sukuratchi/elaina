import discord, os, asyncio, random, array
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands

load_dotenv()

TOKEN = os.getenv('TOKEN')
loadedCogs = []
MY_GUILD = discord.Object(id=850093371073757194)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents, application_id='991731064026448043', guilds=[discord.Object(id=850093371073757194)])

@bot.event
async def on_ready():
    change_status.start()
    bot.tree.copy_global_to(guild = MY_GUILD)
    await bot.tree.sync(guild = MY_GUILD)
    print(f"Ready for action! Logged in as {bot.user}")

@tasks.loop(seconds=45)
async def change_status():
    statusType = random.randint(0, 5)
    if statusType == 0:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="some anime"))
    elif statusType == 1:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the rain outside"))
    elif statusType == 2:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="vtubers"))
    elif statusType == 3:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="booba"))
    elif statusType == 4:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ"))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="TF2"))

@bot.tree.command(name='sync', description='syncs commands from cogs')
async def sync(interaction: discord.Interaction):
    fmt = await bot.tree.sync(guild = MY_GUILD)
    await interaction.response.send_message(f"Refreshed {len(fmt)} commands.", ephemeral = True)

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            global loadedCogs
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')

@bot.tree.command(name='loaded', description='Checks what cogs are loaded')
async def loaded(interaction: discord.Interaction):
    global loadedCogs
    await interaction.response.send_message(f"{loadedCogs} are loaded!", ephemeral = True)

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())