import discord
from discord.ext import commands
import helper as hp

class Reddit:
    def __init__(self, client):
        self.client = client

    # Quick implemented shortcut commands
    @commands.command(pass_context=True)
    async def meme(self, ctx):
        url = "https://api.reddit.com/user/pete7201/m/dankmemenetwork/top.json?sort=top&t=day&limit=100"
        await self.client.send_message(ctx.message.channel, embed=hp.redditEmbed(url))

    @commands.command(pass_context=True)
    async def joke(self, ctx):
        url = "https://api.reddit.com/r/Jokes/top.json?sort=top&t=day&limit=100"
        await self.client.send_message(ctx.message.channel, embed=hp.redditEmbed(url))

    @commands.command(pass_context=True)
    async def shitpost(self, ctx):
        url = "https://api.reddit.com/r/copypasta/top/.json?sort=top&t=week&limit=100"
        await self.client.send_message(ctx.message.channel, embed=hp.redditEmbed(url))

    @commands.command(pass_context=True)
    async def wholesome(self, ctx):
        url = "https://api.reddit.com/r/wholesomememes/top/.json?sort=top&t=week&limit=100"
        await self.client.send_message(ctx.message.channel, embed=hp.redditEmbed(url))

    @commands.command(pass_context=True)
    async def pun(self, ctx):
        url = "https://api.reddit.com/r/puns/top/.json?sort=top&t=week&limit=100"
        await self.client.send_message(ctx.message.channel, embed=hp.redditEmbed(url))

    # Custom reddit post embedder
    @commands.command(pass_context=True)
    async def reddit(self, ctx, subr = None):
        if subr == None:
            await self.client.send_message(ctx.message.channel, ctx.message.author.mention + " Please specify a subreddit.")
        else:
            url = "https://api.reddit.com/r/" + subr + "/top/.json?sort=top&t=week&limit=100"
            await self.client.send_message(ctx.message.channel, embed=hp.redditEmbed(url))

def setup(client):
    client.add_cog(Reddit(client))