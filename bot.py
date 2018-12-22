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

@client.command()
async def meme():
    response = requests.get("https://api.reddit.com/r/dankmemes.json?sort=top&t=day&limit=100").json()
    # print(response["data"]["children"][0]["data"]["title"])
    post = response["data"]["children"][random.randint(1,100)]
    # print(post["data"]["title"])
    meme = discord.Embed(
        title = post["data"]["title"],
        colour = discord.Colour.blue(),
        image = "https://testcreative.co.uk/wp-content/uploads/2017/10/Test-Logo-Circle-black-transparent.png"
    )
    await client.send_message(ctx.message.channel, embed=meme)

@client.command(pass_context=True)
async def sound(ctx, file):
    if not os.path.exists('./assets/' + file + '.mp3'):
        await client.say("{} This sound doesn't exist bruh".format(ctx.message.author.mention))
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
            await client.say('{} Join a voice channel fam'.format(ctx.message.author.mention))

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

# @client.event
# async def on_message(message):
#     author = message.author
#     content = message.content
#     channel = message.channel
#     print('{}: {}'.format(author, content))
#     #await client.send_message(channel, )

client.run(TOKEN)
