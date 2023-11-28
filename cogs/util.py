import discord, random, os, platform, psutil
from discord import app_commands
from discord.ext import commands
from math import floor

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility cog loaded!")

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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        responses = [
            f"Lets all welcome <@!{member.id}> to the server!",
            f"Hey look, <@!{member.id}> has joined the server!",
            f"Hi there <@!{member.id}>! Hope you enjoy your stay here.",
            f"Welcome to the server, <@!{member.id}>!",
            f"A new face, <@!{member.id}>, has arrived. Welcome in!"
        ]
        myguild = self.bot.get_guild(1116469018019233812)
        welcome = myguild.get_channel(1178850385901932564)
        role = myguild.get_role(1179086276935299164)
        await member.add_roles(role)
        await welcome.send(random.choice(responses))
        
async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1116469018019233812)])