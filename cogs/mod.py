import discord
from discord import app_commands
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod cog loaded!")

    @app_commands.command(name="ban", description="Ban command")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Done!", ephemeral=True)

    @ban.error
    async def on_ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod(bot), guilds=[discord.Object(id=850093371073757194)])