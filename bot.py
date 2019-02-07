import discord
import os
import json
import requests
import random
import glob
from difflib import SequenceMatcher
from googletrans import Translator
from googletrans import LANGUAGES
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio


import config as cfg
TOKEN = cfg.TOKEN

client = commands.Bot(command_prefix = 'pls ')
client.remove_command('help')

async def reply(ctx, str = None):
    await client.send_message(ctx.message.channel, "{} ".format(ctx.message.author.mention) + str)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type "pls help" for more info'))
    print('bot is ready')

@client.event
async def on_message(message):
    print(message.channel.name)
    if message.author != client.user and message.channel.name == 'autimatic-text-to-speech':
        await client.send_message(message.channel, message.content, tts=True)
    await client.process_commands(message)

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
        await reply(ctx, "Please specify a subreddit.")
    else:
        url = "https://api.reddit.com/r/" + subr + "/top/.json?sort=top&t=week&limit=100"
        await client.send_message(ctx.message.channel, embed=redditEmbed(url))

#----------------------------------------------------------------------------------#



@client.command(pass_context=True)
async def translate(ctx, text = None, target = None):
    found = False
    maxim = -1
    similar = ""
    for key in LANGUAGES:
        if target == LANGUAGES[key] or target == key:
            found = True
        elif SequenceMatcher(None, LANGUAGES[key], target).ratio() > maxim:
            similar = LANGUAGES[key]
            maxim = SequenceMatcher(None, LANGUAGES[key], target).ratio()
    if found:
        translation = Translator().translate(text, dest=target)
        print(translation)
        await reply(ctx, "`Language detected: " + translation.src + "` \n" + translation.origin + " ` -> ` " + translation.text)
    else:
        await reply(ctx, "Language not found, did you mean ***" + similar + "***? For a list of available languages, type `pls help`")


@client.command(pass_context=True)
async def sound(ctx, file = None):
    if file == None:
        await reply(ctx, "Please specify a sound.")
    elif file == 'list':
        files = ", ".join(glob.glob("./assets/*.mp3"))
        await reply(ctx, "Heres all the sounds I found: "+files.replace('./assets/', '').replace('.mp3', ''))
    elif not os.path.exists('./assets/' + file + '.mp3'):
        await reply(ctx, "The sound file `" + file + "` does not exist.")
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
            await reply(ctx, "Join a voice channel first.")

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
