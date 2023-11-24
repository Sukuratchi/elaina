import discord, os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
slash = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await slash.sync(guild=discord.Object(id=925142628847218698))
    print(f"Ready for action! Logged in as {client.user}")

@slash.command(name = "test", description = "testing", guild=discord.Object(id=925142628847218698))
async def first_command(interaction):
    await interaction.response.send_message("Hi there!")

client.run(TOKEN)