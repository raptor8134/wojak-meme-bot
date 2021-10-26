import discord
from discord.ext import commands
from os import getenv
import io

from meme import * 

def bot_url():
    client_id = getenv("D_CLIENT_ID")
    permissions = getenv("D_PERMISSIONS")
    print("https://discord.com/api/oauth2/authorize?client_id=" + client_id + "&scope=bot&permissions=" + permissions)

def discord_meme(memes, meme, arguments):
    text = ' '.join(arguments)
    #file = io.BytesIO()
    #memes[meme](text).save(file, "jpeg")
    #image = discord.File(file)
    memes[meme](text).save("tmp.jpg")
    image = discord.File("tmp.jpg")
    print("made a '" + meme + "' meme")
    return image


def discordbot(memes):
    bot = commands.Bot(command_prefix="!")
    token = getenv("D_TOKEN")

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="with your balls"))
        print("Ready!")

    @bot.command()
    async def soyjack(ctx, *args):
        image = discord_meme(memes, 'soyjack', args)
        await ctx.send(file=image)

    @bot.command()
    async def gigachad(ctx, *args):
        image = discord_meme(memes, 'gigachad', args)
        await ctx.send(file=image)

    @bot.command()
    async def chadyes(ctx, *args):
        image = discord_meme(memes, 'chadyes', args)
        await ctx.send(file=image)

    @bot.command()
    async def chadno(ctx, *args):
        image = discord_meme(memes, 'chadno', args)
        await ctx.send(file=image)

    bot.run(token)
