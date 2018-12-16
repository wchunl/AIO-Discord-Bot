import discord

from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio

TOKEN = 'NDg1MjM5ODU2ODM1MDY3OTM1.Dtj5oA.u8Uqk4ZRu-AOO8ohdHvaIUm0DE8'

client = commands.Bot(command_prefix = 'pls ')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type "pls help" for more info'))
    print('bot is ready')


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