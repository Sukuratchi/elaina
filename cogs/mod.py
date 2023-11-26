import discord
from discord import app_commands
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod cog loaded!")

    @app_commands.command(name = "ban", description = "Ban command")
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "None given"):
        embed = discord.Embed(
            title=f"Member banned!", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name = "Member", value = f"<@!{member.id}>")
        embed.add_field(name = "Performed by", value=f"<@!{interaction.user.id}>")
        embed.add_field(name = "Reason", value = reason)

        myguild = self.bot.get_guild(850093371073757194)
        modlog = myguild.get_channel(1177953545681649714)
        await modlog.send(embed=embed)

        await member.ban(reason=reason)
        await interaction.response.send_message(f"Done! Banned {member}", ephemeral=True)

    @ban.error
    async def on_ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

    @app_commands.command(name="kick", description="Kick command")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "None given"):
        embed = discord.Embed(
            title=f"Member kicked!", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name = "Member", value = f"<@!{member.id}>")
        embed.add_field(name = "Performed by", value=f"<@!{interaction.user.id}>")
        embed.add_field(name = "Reason", value = reason)

        myguild = self.bot.get_guild(850093371073757194)
        modlog = myguild.get_channel(1177953545681649714)
        await modlog.send(embed=embed)

        await member.kick(reason=reason)
        await interaction.response.send_message(f"Done! Kicked {member}", ephemeral=True)

    @kick.error
    async def on_kick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"You're not allowed to run this command. Sorry!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod(bot), guilds=[discord.Object(id=850093371073757194)])