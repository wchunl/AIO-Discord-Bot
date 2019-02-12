import discord
import json
import requests
import random


# Skeleton function for embedding reddit posts
def redditEmbed(url):
    response = requests.get(url, headers = {'User-agent': 'test'}).json()
    error = discord.Embed(colour = discord.Colour.red(), description = "This subreddit doesn't exist or it is private.")
    try:
        if not response["data"]["dist"] < 100:
            post = response["data"]["children"][random.randint(1,99)]
            embed = discord.Embed(
                title = post["data"]["title"],
                description = post["data"]["selftext"],
                colour = discord.Colour.blue()
            )
            embed.set_image(url=post["data"]["url"])
            embed.set_footer(text='Posted by ' + post["data"]["author_fullname"])
            return (embed)
        else:
            return error
    except KeyError:
        return error