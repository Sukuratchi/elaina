import discord, random, os, platform, psutil
from discord import app_commands
from discord.ext import commands, tasks
from math import floor

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Utility cog loaded!")

    @tasks.loop(seconds=30)
    async def change_status(self):
        statusType = random.randint(0, 6)
        match statusType:
            case 0:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="some anime"))        
            case 1:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the rain outside"))
            case 2:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="vtubers"))
            case 3:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="booba"))
            case 4:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ ᵇᵉᵃⁿ"))
            case 5:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="smol crimes"))
            case 6:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="TF2"))

    @app_commands.command(name='ping', description='Checks bot ping')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! Response is at a blazing fast {round(self.bot.latency * 1000)}ms')

    @app_commands.command(name='stats', description='Shows the stats of the bot')
    async def stats(self, interaction: discord.Interaction):
        process = psutil.Process(os.getpid())

        embed = discord.Embed(
            title=f"{self.bot.user.name} Statistics", color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="Memory Usage",
                        value=f"{floor(process.memory_info().rss/1000/1000)} MB")
        embed.add_field(name="Python Version", value=platform.python_version())

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name = 'avatar', description = 'Gets your own or a users avatar')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member):
        avatar = member.display_avatar
        await interaction.response.send_message(f"Here's your [avatar!]({avatar})")

    @app_commands.command(name = 'banner', description = 'Gets your own or a users avatar')
    async def banner(self, interaction: discord.Interaction, member: discord.Member):
        user = await self.bot.fetch_user(member.id)
        banner = user.banner.url
        await interaction.response.send_message(f"Here's your [banner!]({banner})")

    @banner.error
    async def on_banner_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message("This command failed! Try making sure you have a banner (you need regular nitro for this (not basic)).\nIf you're sure that the user has a banner, please ping _Sukuratchi about this", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1116469018019233812)])