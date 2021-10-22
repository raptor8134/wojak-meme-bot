import discord
from discord.ext import commands
from os import getenv
import io

from meme import * 

def bot_url():
    client_id = getenv("D_CLIENT_ID")
    permissions = getenv("D_PERMISSIONS")
    print("https://discord.com/api/oauth2/authorize?client_id=" + client_id + "&scope=bot&permissions=" + permissions)

def discordbot(memes):
    bot = commands.Bot(command_prefix="!")
    token = getenv("D_TOKEN")

    @bot.event
    async def on_ready():
        print("Spinning up ...")

    @bot.command(aliases=["rebuke"])
    async def soyjack(ctx, *args):
        text = " ".join(args)
        angrysoyjack(text).save("tmp.jpg")
        image = discord.File("tmp.jpg")
        await ctx.send(file=image)

    bot.run(token)
