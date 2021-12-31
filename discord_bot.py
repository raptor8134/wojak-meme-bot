import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from sys import argv
from wojak_generator.templates import Templates
from wojak_generator.render import PhotoRender
from wojak_generator.helpers import PILToBytes, checkEnv

def bot_url():
    client_id = getenv("D_CLIENT_ID")
    permissions = getenv("D_PERMISSIONS")
    print("https://discord.com/api/oauth2/authorize?client_id=" + client_id + "&scope=bot&permissions=" + permissions)

def discord_meme(memes: list, meme: str, arguments: list)-> discord.File:
    text = ' '.join(arguments)
    texts = [text]
    # Path to template img
    path = f'{templates.base}/{meme}'
    # Template config
    template = templates.one(meme)
    render = PhotoRender(path, template)
    img = render.getImage()
    byte_im = PILToBytes(img)
    image = discord.File(fp=byte_im, filename='meme.jpg')
    print("made a '" + meme + "' meme")
    return image

def discordbot():
    bot = commands.Bot(command_prefix="!")
    token = getenv("D_TOKEN")
    templates = Templates()
    memes = templates.all()

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="with your balls"))
        print("Started Discord Bot!")

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

if __name__ == '__main__':
    load_dotenv()
    if argv[1] == '--url':
        required_env = [
            "D_CLIENT_ID", "D_PERMISSIONS"
        ]
        checkEnv(required_env)
        bot_url()
    else:
        required_env = [
            "D_TOKEN"
        ]
        checkEnv(required_env)
        discordbot()
