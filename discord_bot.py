import discord
from discord.ext import commands
from os import getenv

from meme import * 
from imgur import *

def discordbot(memes):
    bot = commands.Bot(command_prefix="!")
    token = getenv("D_TOKEN")

    @bot.event
    async def ready():
        print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")


    #
    #
    #

    bot.run(token)
