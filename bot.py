import discord
import os
import json
import requests
import random

from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio


import config as cfg
TOKEN = cfg.TOKEN

client = commands.Bot(command_prefix = 'pls ')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type "pls help" for more info'))
    print('bot is ready')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    embed.set_author(name='Help')
    embed.add_field(name='.ping', value="Returns Pong!", inline=False)
    await client.send_message(author, embed=embed)

#####################################################################################
#####                              REDDIT COMMANDS                              #####
#####################################################################################
# Skeleton for embedding reddit posts
def redditEmbed(url):
    response = requests.get(url, headers = {'User-agent': 'test'}).json()
    if response["data"]["dist"] < 100:
        return discord.Embed(colour = discord.Colour.red(), description = "The subreddit doesn't exist/work!")
    else:
        post = response["data"]["children"][random.randint(1,100)]
        embed = discord.Embed(
            title = post["data"]["title"],
            description = post["data"]["selftext"],
            colour = discord.Colour.blue()
        )
        embed.set_image(url=post["data"]["url"])
        embed.set_footer(text='Posted by ' + post["data"]["author_fullname"])
        return (embed)

# Quick implemented shortcut commands
@client.command(pass_context=True)
async def meme(ctx):
    url = "https://api.reddit.com/user/pete7201/m/dankmemenetwork/top.json?sort=top&t=day&limit=100"
    await client.send_message(ctx.message.channel, embed=redditEmbed(url))

@client.command(pass_context=True)
async def joke(ctx):
    url = "https://api.reddit.com/r/Jokes/top.json?sort=top&t=day&limit=100"
    await client.send_message(ctx.message.channel, embed=redditEmbed(url))

@client.command(pass_context=True)
async def shitpost(ctx):
    url = "https://api.reddit.com/r/copypasta/top/.json?sort=top&t=week&limit=100"
    await client.send_message(ctx.message.channel, embed=redditEmbed(url))

@client.command(pass_context=True)
async def wholesome(ctx):
    url = "https://api.reddit.com/r/wholesomememes/top/.json?sort=top&t=week&limit=100"
    await client.send_message(ctx.message.channel, embed=redditEmbed(url))

@client.command(pass_context=True)
async def puns(ctx):
    url = "https://api.reddit.com/r/puns/top/.json?sort=top&t=week&limit=100"
    await client.send_message(ctx.message.channel, embed=redditEmbed(url))

# Custom reddit post embedder
@client.command(pass_context=True)
async def reddit(ctx, subr = None):
    if subr == None:
        await client.send_message(ctx.message.channel, "{} Specify a subreddit bro".format(ctx.message.author.mention))
    else:
        url = "https://api.reddit.com/r/" + subr + "/top/.json?sort=top&t=week&limit=100"
        await client.send_message(ctx.message.channel, embed=redditEmbed(url))

#----------------------------------------------------------------------------------#


@client.command(pass_context=True)
async def sound(ctx, file = None):
    if file == None:
         await client.send_message(ctx.message.channel, "{} Specify a sound bro".format(ctx.message.author.mention))
    if not os.path.exists('./assets/' + file + '.mp3'):
        await client.send_message(ctx.message.channel, "{} That sound doesn't exist bruh".format(ctx.message.author.mention))
    else:
        channel = ctx.message.author.voice.voice_channel
        if channel != None:
            vc = await client.join_voice_channel(channel)
            player = vc.create_ffmpeg_player('./assets/' + file + '.mp3')
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)
            player.stop()
            await vc.disconnect()
        else:
            await client.send_message(ctx.message.channel, '{} Join a voice channel fam'.format(ctx.message.author.mention))

@client.command()
async def ping():
    await client.say('Pong!')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

client.run(TOKEN)
