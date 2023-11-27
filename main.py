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

async def loadCogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')

@bot.tree.command(name='loaded', description='Checks what cogs are loaded')
async def loaded(interaction: discord.Interaction):
    await interaction.response.send_message(f"{loadedCogs} are loaded!", ephemeral = True)

@bot.tree.command(name = 'unload', description = 'unloads a cog')
async def unload(interaction: discord.Interaction, cog: str):
    await bot.unload_extension(f"cogs.{cog}")
    loadedCogs.remove(cog)
    await interaction.response.send_message(f"Unloaded {cog}", ephemeral = True)

@bot.tree.command(name = 'load', description = 'Loads a cog')
async def load(interaction: discord.Interaction, cog: str):
    for file in os.listdir('./cogs'):
        if file.startswith(cog):
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')
            await interaction.response.send_message(f"Loaded {cog}", ephemeral = True)

@bot.tree.command(name = 'reload', description = 'Reloads a cog')
async def reload(interaction: discord.Interaction, cog: str):
    await bot.reload_extension(f"cogs.{cog}")
    await interaction.response.send_message(f"Reloaded {cog}!", ephemeral = True)

async def main():
    await loadCogs()
    await bot.start(TOKEN)

asyncio.run(main())