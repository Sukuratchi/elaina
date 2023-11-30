import discord, os, requests, asyncio
from discord.ext import commands, tasks
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
            return stream
        else:
            return "OFFLINE"
    except Exception as e:
        return "An error occured: " + str(e)
    
class TwitchTrack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.twitchNotif.start()
        print("Twitch tracking cog loaded!")

    @tasks.loop(seconds = 30)
    async def twitchNotif(self):
        global isLive
        stream = checkIfLive("sukuratchiii")
        if stream != "OFFLINE":
            asyncio.sleep(5)
            if stream != "OFFLINE":
                if isLive == False:
                    isLive = True
                    #myguild = self.bot.get_guild(1116469018019233812)
                    #live = myguild.get_channel(1120845503941320776)
                    #await live.send("_Sukuratchi is live! [Come watch here!](https://twitch.tv/sukuratchiii)")
                    print("Live notification")
        else:
            if isLive == True:
                isLive = False
                #myguild = self.bot.get_guild(850093371073757194)
                #live = myguild.get_channel(1177953545681649714)
                #await live.send("_Sukuratchi went offline.")

async def setup(bot):
    await bot.add_cog(TwitchTrack(bot), guilds=[discord.Object(id=1116469018019233812)])