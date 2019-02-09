import discord
import os
import json
import requests
import random
import glob
import datetime
from difflib import SequenceMatcher
from googletrans import Translator
from googletrans import LANGUAGES
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio


import config as cfg
TOKEN = cfg.TOKEN

client = commands.Bot(command_prefix = 'pls ', case_insensitive=True)
client.remove_command('help')

async def reply(ctx, str = None):
    await client.send_message(ctx.message.channel, "{} ".format(ctx.message.author.mention) + str)

def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            return channel
    return None

def get_similar(keyword, list):
    maxim = -1
    result = None
    for key in list:
        if SequenceMatcher(None, keyword, key).ratio() > maxim:
            maxim = SequenceMatcher(None, keyword, key).ratio()
            result = key
    if result == None:
        return " "
    else:
        return ", did you mean ***" + result + "***?"

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type "pls help" for more info'))
    print('bot is ready')
    url = "https://api.reddit.com/user/pete7201/m/dankmemenetwork/top.json?sort=top&t=day&limit=100"
    while True:
        await asyncio.sleep(60*60*12) #every minute
        chanl = get_channel(client.get_all_channels(), 'bots')
        await client.send_message(chanl, "TODAYS DAILY MEME: ")
        await client.send_message(chanl, embed=redditEmbed(url))

@client.event
async def on_message(message):
    if message.author != client.user:
        if  message.channel.name == 'autimatic-text-to-speech':
            print("place holder")
            # await client.send_message(message.channel,  .content, tts=True)
        elif message.content.startswith("pls") or message.content.startswith("Pls"):
            print(message.content)
            if message.channel.name == 'bots':
                await client.process_commands(message)
            else:
                await client.send_message(message.channel, "Please use the `bots` text channel.")

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await reply(ctx, "Command not found, did you mean `pls " + get_similar(ctx.message.content, client.commands) + "`? For a list of commands type `pls help`.")
    else:
        print(error)
        await reply(ctx, "An error occured, please try again.")

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        title = 'Commands List',
        description = 'All commands are called with the prefix `pls`. Replace the brackets [arg] with your desired input',
        colour = discord.Colour.blue()
    )
    embed.set_author(name='Dench Memer v2.0')
    embed.add_field(name='General Commands', value="=====================", inline=False)
    embed.add_field(name='>> `pls sound [name]`', value="Plays a soundboard, must be in a voice channel, type `pls sound list` for a list of sounds", inline=False)
    embed.add_field(name='>> `pls translate "[text]" "[soruce]"`', value="Translate [text] to [source] language, type `pls langs` for a list of languages", inline=False)
    embed.add_field(name='Reddit Commands', value="=====================", inline=False)
    embed.add_field(name='>> `pls meme`', value="Sends a dank meme")
    embed.add_field(name='>> `pls joke`', value="Sends a dank joke")
    embed.add_field(name='>> `pls shitpost`', value="Sends a dank shitpost")
    embed.add_field(name='>> `pls wholesome`', value="Sends a wholesome meme")
    embed.add_field(name='>> `pls pun`', value="Sends a dank pun")
    embed.add_field(name='>> `pls reddit [subreddit]`', value="Sends a random post from a given subreddit", inline=False)
    embed.add_field(name='Misc Commands', value="=====================", inline=False)
    embed.add_field(name='>> `pls echo "[text]"`', value="Repeats the message", inline=False)
    embed.add_field(name='>> `pls ping`', value="Ping Pong command", inline=False)
    await client.send_message(author, embed=embed)
    await reply(ctx, "Sent you a dm.")

#####################################################################################
#####                              REDDIT COMMANDS                              #####
#####################################################################################
# Skeleton for embedding reddit posts
def redditEmbed(url):
    response = requests.get(url, headers = {'User-agent': 'test'}).json()
    # print(response["data"])
    valid = False
    try:
        response["data"]["dist"]
        valid = True
    except KeyError:
        valid = False
    if not valid:
        return discord.Embed(colour = discord.Colour.red(), description = "This subreddit is private!")
    elif response["data"]["dist"] < 100:
        return discord.Embed(colour = discord.Colour.red(), description = "This subreddit doesn't exist/work!")
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
async def pun(ctx):
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

#####################################################################################
#####                             GENERAL COMMANDS                              #####
#####################################################################################


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
        await reply(ctx, "Language not found, did you mean ***" + similar + "***? For a list of available languages, type `pls langs`")

@client.command(pass_context=True)
async def langs(ctx):
    langs = []
    key = []
    for key in LANGUAGES:
        langs.append(LANGUAGES[key])
    embed = discord.Embed(
        title = "Here's a list of all available languages: ",
        description = ", ".join(langs),
        colour = discord.Colour.blue()
    )
    await client.send_message(ctx.message.author, embed=embed)
    await reply(ctx, "Sent you a dm.")

@client.command(pass_context=True)
async def sound(ctx, file = None):
    files = [os.path.splitext(os.path.basename(x))[0] for x in glob.glob('./assets/*.mp3')]
    print(files)
    if file == None:
        await reply(ctx, "Please specify a sound.")
    elif file == 'list':
        await reply(ctx, "Heres all the sounds I found: " + files)
    elif not os.path.exists('./assets/' + file + '.mp3'):
        await reply(ctx, "Could not find sound `" + file + "`, did you mean `" + get_similar(file,files) + "`?")
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

#####################################################################################
#####                               MISC COMMANDS                               #####
#####################################################################################

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
