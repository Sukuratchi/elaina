import discord, os, asyncio, random, array
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands

load_dotenv()

TOKEN = os.getenv('TOKEN')
loadedCogs = []
MY_GUILD = discord.Object(id=1116469018019233812)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents, application_id='991731064026448043', guilds=[discord.Object(id=1116469018019233812)])

@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild = MY_GUILD)
    await bot.tree.sync(guild = MY_GUILD)
    print(f"Ready for action! Logged in as {bot.user}")

@bot.tree.command(name='sync', description='syncs commands from cogs')
@app_commands.checks.has_role(1120840113170157599)
async def sync(interaction: discord.Interaction):
    fmt = await bot.tree.sync(guild = MY_GUILD)
    await interaction.response.send_message(f"Refreshed {len(fmt)} commands.", ephemeral = True)

@sync.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

@bot.tree.command(name='loaded', description='Checks what cogs are loaded')
@app_commands.checks.has_role(1120840113170157599)
async def loaded(interaction: discord.Interaction):
    await interaction.response.send_message(f"{loadedCogs} are loaded!", ephemeral = True)

@loaded.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

@bot.tree.command(name = 'unload', description = 'unloads a cog')
@app_commands.checks.has_role(1120840113170157599)
async def unload(interaction: discord.Interaction, cog: str):
    await bot.unload_extension(f"cogs.{cog}")
    loadedCogs.remove(cog)
    await interaction.response.send_message(f"Unloaded {cog}", ephemeral = True)
    print(f"Unloaded {cog}")

@unload.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

@bot.tree.command(name = 'load', description = 'Loads a cog')
@app_commands.checks.has_role(1120840113170157599)
async def load(interaction: discord.Interaction, cog: str):
    for file in os.listdir('./cogs'):
        if file.startswith(cog):
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')
            await interaction.response.send_message(f"Loaded {cog}", ephemeral = True)
            print(f"Loaded {cog}")

@load.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

@bot.tree.command(name = 'reload', description = 'Reloads a cog')
@app_commands.checks.has_role(1120840113170157599)
async def reload(interaction: discord.Interaction, cog: str):
    await bot.reload_extension(f"cogs.{cog}")
    await interaction.response.send_message(f"Reloaded {cog}!", ephemeral = True)
    print(f"Reloaded {cog}")

@reload.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

async def loadCogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await loadCogs()
    await bot.start(TOKEN)

asyncio.run(main())