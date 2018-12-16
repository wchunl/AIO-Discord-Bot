import discord

from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio

TOKEN = #snipped

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

@client.command(pass_context=True)
async def sound(ctx):
    # discord.opus.load_opus(name)
    channel = ctx.message.author.voice.voice_channel
    if channel != None:
        vc = await client.join_voice_channel(channel)
        player = vc.create_ffmpeg_player('./assets/clap.mp3')
        player.start()
        # print('started')
        while not player.is_done():
            await asyncio.sleep(1)
        player.stop()
        await vc.disconnect()
    else:
        await client.say('Please join a voice channel first!')

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
