import discord, random, os, platform, psutil
from discord import app_commands
from discord.ext import commands, tasks
from math import floor

import requests, os
from dotenv import load_dotenv

load_dotenv()
client_secret = os.getenv('clientSecret')
client_id = os.getenv('clientID')

isLive = False

class Stream:

    def __init__(self, title, streamer, game):
        self.title = title
        self.streamer = streamer
        self.game = game
        
# getting the auth token from the twitch API
def getOAuthToken():
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)

    #data output
    keys = r.json()
    return keys['access_token']

def checkIfLive(channel):
    # Calling the twitch api to check if a specific is live
    url = "https://api.twitch.tv/helix/streams?user_login=" + channel
    token = getOAuthToken()

    HEADERS = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + token
    }

    try:
        
        req = requests.get(url, headers=HEADERS)
        
        res = req.json()

        if len(res['data']) > 0: # the twitch channel is live
            data = res['data'][0]
            title = data['title']
            streamer = data['user_name']
            game = data['game_name']
            thumbnail_url = data['thumbnail_url']
            stream = Stream(title, streamer, game, thumbnail_url)
            #stream = Stream(title, streamer, game)
            return stream
        else:
            return "OFFLINE"
    except Exception as e:
        return "An error occured: " + str(e)

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.twitchNotif.start()
        print("Utility cog loaded!")

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Refreshed {len(fmt)} commands!")

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
            f"Hi there <@!{member.id}>! Hope you enjoy your stay here."
        ]
        myguild = self.bot.get_guild(850093371073757194)
        welcome = myguild.get_channel(865340222581899284)
        await welcome.send(random.choice(responses))

    @tasks.loop(seconds = 10)
    async def twitchNotif(self):
        #print("Running loop")
        global isLive
        stream = checkIfLive("sukuratchiii")
        if stream != "OFFLINE":
            #print("Checking if stream is live")
            if isLive == False:
                isLive = True
                myguild = self.bot.get_guild(850093371073757194)
                modlog = myguild.get_channel(1177953545681649714)
                await modlog.send("_Sukuratchi is live!")
                #print("Channel is live!")
        else:
            #print("Checking if stream is not live")
            if isLive == True:
                isLive = False
                myguild = self.bot.get_guild(850093371073757194)
                modlog = myguild.get_channel(1177953545681649714)
                await modlog.send("_Sukuratchi went offline.")
                #print("Channel is not live!")
        
async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=850093371073757194)])