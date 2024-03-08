import discord
import re
from discord.ext import commands


async def fix_pixiv(message: discord.Message, link: str):
    link = link.replace("www.", "")
    link = link.replace("pixiv.net", "phixiv.net")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)


async def fix_reddit(message: discord.Message, link: str):
    link = link.replace("www.", "")
    link = link.replace("reddit.com", "rxddit.com")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)


async def fix_twitter(message: discord.Message, link: str):
    link = link.replace("www.", "")
    link = link.replace("x.com", "twitter.com")
    link = link.replace("twitter.com", "vxtwitter.com")

    await message.reply(f"Here's a better link! {link}", mention_author=False)
    await message.edit(suppress=True)


class Socialfix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.twitter_pattern = re.compile(r"(https://(www.)?(twitter|x)\.com/[a-zA-Z0-9_]+/status/[0-9]+)")
        self.pixiv_pattern = re.compile(r"(https://(www.)?(pixiv)\.net/en/artworks/[0-9]+)")
        self.reddit_pattern = re.compile(r"(https://(www.)?(reddit)\.com/r/[^/]+/(?:comments|s)/[a-zA-Z0-9]+/?)")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Socialfix cog is here!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        message_content = message.content.strip("<>")
        if twitter_match := self.twitter_pattern.search(message_content):
            link = twitter_match.group(0)
            await fix_twitter(message, link)
        elif pixiv_match := self.pixiv_pattern.search(message_content):
            link = pixiv_match.group(0)
            await fix_pixiv(message, link)
        elif reddit_match := self.reddit_pattern.search(message.content):
            link = reddit_match.group(0)
            await fix_reddit(message, link)


async def setup(bot):
    await bot.add_cog(Socialfix(bot), guilds=[discord.Object(id=1116469018019233812)])
