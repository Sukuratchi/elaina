import discord
from discord import app_commands
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility cog loaded!")

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Refreshed {len(fmt)} commands!")

    @app_commands.command(name='ping', description='Checks bot ping')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! Response is at a blazing fast {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=850093371073757194)])