import discord
import os
import glob
import datetime
import helper as hp
from difflib import SequenceMatcher
from googletrans import Translator
from googletrans import LANGUAGES
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio


import config as cfg
TOKEN = cfg.TOKEN
REDACTABLE = cfg.REDACTABLE
extensions = cfg.EXTENSIONS

client = commands.Bot(command_prefix = 'pls ', case_insensitive=True)
client.remove_command('help')


async def reply(ctx, str = ""):
    await client.send_message(ctx.message.channel, "{} ".format(ctx.message.author.mention) + str)

def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            return channel
    return None

def get_similar(keyword, list):
    maxim = 0.5
    result = None
    for key in list:
        if SequenceMatcher(None, keyword, key).ratio() > maxim:
            maxim = SequenceMatcher(None, keyword, key).ratio()
            result = key
    if result == None:
        return "."
    else:
        return ", did you mean `" + result + "`?"

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type "pls help" for more info'))
    print('Running an instance of ' + client.user.name + ' {' + client.user.id + '}')
    print('Bot is ready. \n -----------------------------------------------')
    url = "https://api.reddit.com/user/pete7201/m/dankmemenetwork/top.json?sort=top&t=day&limit=100"
    chanl = get_channel(client.get_all_channels(), 'bots')

    while True:
        await asyncio.sleep(60*60*24) #every 24 hours
        embed = hp.redditEmbed(url)
        embed.set_author(name="~~~~~ TODAY'S DAILY MEME ~~~~~")
        await client.send_message(chanl, embed=embed)

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author != client.user and message.content.startswith("pls"):
        if len(message.content) < 4:
            await client.send_message(message.channel, "{} Please specify a command.".format(message.author.mention))
        elif  message.channel.name == 'autimatic-text-to-speech':
            print("place holder")
            # await client.send_message(message.channel, message.content, tts=True)
        elif message.channel.name == 'bots':
            await client.process_commands(message)
        else:
            await client.send_message(message.channel, "{} Please use the `bots` text channel.".format(message.author.mention))

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await reply(ctx, "Command not found" + get_similar(ctx.message.content, client.commands) + " For a list of commands type `pls help`.")
    else:
        print(error)
        await reply(ctx, "An error occured, please try again.")

@client.command(pass_context=True)
async def translate(ctx, text = None, target = None):
    if text == None or target == None:
        await reply(ctx, "The text or target field is missing! For more information, type `pls help`")
    else:
        found = False
        maxim = -1
        similar = ""
        if target == "chinese":
            msg = await client.send_message(ctx.message.channel, "{} 🇸implified or 🇹raditional?".format(ctx.message.author.mention))
            await client.add_reaction(msg, '🇸')
            await client.add_reaction(msg, '🇹')
            res = await client.wait_for_reaction(['🇸', '🇹'], message=msg, user=ctx.message.author)
            if str(res.reaction.emoji) == '🇸':
                target = "chinese (simplified)"
            elif res.reaction.emoji == '🇹':
                target = "chinese (traditional)"

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
            await reply(ctx, "Language not found, did you mean `" + similar + "`? For a list of available languages, type `pls langs`")

@client.command(pass_context=True)
async def langs(ctx):
    langs = []
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
    if file == None:
        await reply(ctx, "Please specify a sound.")
    elif file == 'list':
        await reply(ctx, "Heres all the sounds I found: " + ', '.join(files))
    elif not os.path.exists('./assets/' + file + '.mp3'):
        await reply(ctx, "Could not find this sound file" + get_similar(file,files) + " For a list of sounds, type `pls sound list`")
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

# loads all extensions here
if __name__ == "__main__":
    print(' ----------------------------------------------')
    print("Loading Extensions...")
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(">" + extension + ".py loaded.")
        except Exception as e:
            print('{} cannot be loaded. [{}]'.format(extension,e))
    print("All extensions loaded. \n ----------------------------------------------")
    client.run(TOKEN)