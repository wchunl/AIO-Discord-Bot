import discord
from discord.ext import commands

class Help:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title = 'Commands List',
            description = 'All commands are called with the prefix `pls`. Replace the brackets [arg] with your desired input',
            colour = discord.Colour.blue()
        )
        embed.set_author(name='Dench Memer v2.1')
        embed.add_field(name='----General Commands----', value="=====================", inline=False)
        embed.add_field(name='>> `pls sound [name]`', value="Plays a soundboard, must be in a voice channel, type `pls sound list` for a list of sounds", inline=False)
        embed.add_field(name='>> `pls translate "[text]" "[soruce]"`', value="Translate [text] to [source] language, type `pls langs` for a list of languages", inline=False)
        embed.add_field(name='----Reddit Commands----', value="=====================", inline=False)
        embed.add_field(name='>> `pls meme`', value="Sends a dank meme")
        embed.add_field(name='>> `pls joke`', value="Sends a dank joke")
        embed.add_field(name='>> `pls shitpost`', value="Sends a dank shitpost")
        embed.add_field(name='>> `pls wholesome`', value="Sends a wholesome meme")
        embed.add_field(name='>> `pls pun`', value="Sends a dank pun")
        embed.add_field(name='>> `pls reddit [subreddit]`', value="Sends a random post from a given subreddit", inline=False)
        embed.add_field(name='----Misc Commands----', value="=====================", inline=False)
        embed.add_field(name='>> `pls echo "[text]"`', value="Repeats the message", inline=False)
        embed.add_field(name='>> `pls ping`', value="Ping Pong command", inline=False)
        await self.client.send_message(ctx.message.author, embed=embed)
        await self.client.send_message(ctx.message.channel, "{} Sent you a dm.".format(ctx.message.author.mention))

def setup(client):
    client.add_cog(Help(client))