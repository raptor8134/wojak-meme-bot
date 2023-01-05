import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from sys import argv
from io import BytesIO
import logging
import wojak_generator.templates
from wojak_generator.templates import Templates
from wojak_generator.render import PhotoRender
from wojak_generator.helpers import PIL_to_bytes, check_env

def bot_url():
    client_id = getenv("D_CLIENT_ID")
    permissions = getenv("D_PERMISSIONS")
    print("https://discord.com/api/oauth2/authorize?client_id=" + client_id + "&scope=bot&permissions=" + permissions)

async def discord_meme(ctx, meme: str, arguments: list)-> discord.File:
    # template config
    templates = Templates()
    path = f'{templates.base}/{meme}'
    template = templates.one(meme)
    # render image
    render = PhotoRender(path, template)
    render.run(arguments)
    img = render.getImage()
    # send image
    with BytesIO() as img_bin:
        img.save(img_bin, "JPEG")
        img_bin.seek(0)
        image = discord.File(fp=img_bin, filename="meme.jpg")
        await ctx.send(file=image)
    logger.info(f"made a {meme} meme")

def discordbot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    token = getenv("D_TOKEN")

    memes = Templates().memes

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="with your balls"))
        logger.info("Started Discord bot")

    for meme in memes:
        @bot.command(name=meme, pass_context=True)
        async def send_meme(ctx, *args):
            print(ctx.command)
            await discord_meme(ctx, ctx.command, args)

    bot.run(token)

if __name__ == '__main__':
    logger = logging.getLogger("discord_bot")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        handlers = [
            logging.FileHandler("./logs/discord.log"),
            logging.StreamHandler()
        ]
    )

    load_dotenv()
    if len(argv) > 1 and argv[1] == '--url':
        required_env = [
            "D_CLIENT_ID", "D_PERMISSIONS"
        ]
        check_env(required_env)
        bot_url()
    else:
        required_env = [
            "D_TOKEN"
        ]
        check_env(required_env)
        discordbot()
