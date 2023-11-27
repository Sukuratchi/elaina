import discord, re, os, asyncio
from discord.ext import commands

class Socials(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.twitter_pattern = re.compile(r"(https:\/\/(www.)?(twitter|x)\.com\/[a-zA-Z0-9_]+\/status\/[0-9]+)")
        self.pixiv_pattern = re.compile(r"(https:\/\/(www.)?(pixiv)\.net\/en\/artworks\/[0-9]+)")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fix links cog loaded!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        message_content = message.content.strip("<>")
        if twitter_match := self.twitter_pattern.search(message_content):
            link = twitter_match.group(0)
            await self.fix_twitter(message, link)
        elif pixiv_match := self.pixiv_pattern.search(message_content):
            link = pixiv_match.group(0)
            await self.fix_pixiv(message, link)

    async def fix_twitter(self, message: discord.Message, link: str):
        link = link.replace("www.", "")
        link = link.replace('x.com', 'twitter.com')
        link = link.replace("twitter.com", "vxtwitter.com")

        # only fix tweets with an image or video (or links that dont embed at all)
        await asyncio.sleep(1)
        if message.embeds:
            embed = message.embeds[0]
            if embed.to_dict().get('video') or embed.to_dict().get('image'):
                await message.reply(f"Here's a better link: {link}", mention_author=False)
                await asyncio.sleep(0.5)
                await message.edit(suppress=True)
        else:
            await message.reply(f"Here's a better link: {link}", mention_author=False)
            await asyncio.sleep(0.5)
            await message.edit(suppress=True)

    async def fix_pixiv(self, message: discord.Message, link: str):
        link = link.replace("www.", "")
        link = link.replace("pixiv.net", "phixiv.net")

        await message.reply(f"Here's a better link: {link}", mention_author=False)
        await asyncio.sleep(0.5)
        await message.edit(suppress=True)

async def setup(bot):
    await bot.add_cog(Socials(bot), guilds=[discord.Object(id=850093371073757194)])