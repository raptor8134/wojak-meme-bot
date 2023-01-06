import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from sys import argv
from io import BytesIO
import logging
import logging.config
import wojak_generator.templates
from wojak_generator.templates import Templates
from wojak_generator.render.PhotoRender import PhotoRender
from wojak_generator.helpers import PIL_to_bytes, check_env
import colorlogging

def bot_url():
    client_id = getenv("D_CLIENT_ID")
    permissions = getenv("D_PERMISSIONS")
    print(f"https://discord.com/api/oauth2/authorize?client_id={client_id}&scope=bot&permissions={permissions}")

class DiscordBot:
    client: commands.Bot
    token = ""
    memes = []
    templates = []
    templates_list = []
    def __init__(self, token: str):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = commands.Bot(command_prefix="!", intents=intents)
        self.token = token
        self.templates = Templates()
        self.memes = self.templates.memes
        self.templates_list = self.templates.all()

    def get_file(self, ctx: commands.Context, arguments: list)-> discord.File:
        # template stuff
        meme = ctx.command
        path = f"{self.templates.base}/{meme}"
        template = self.templates.one(meme)
        # render image
        render = PhotoRender(template)
        render.run(arguments)
        img = render.get()
        return PIL_to_bytes(img)


    def add_commands(self):
        @self.client.event
        async def on_ready():
            await self.client.change_presence(activity=discord.Game(name="with your balls"))
            logger.info("Started Discord Bot!")

        for meme in self.memes:
            @self.client.command(name=meme, pass_context=True)
            async def send_meme(ctx: commands.Context, *args):
                img = self.get_file(ctx, args)
                with BytesIO(img) as f:
                    image = discord.File(fp=f, filename="meme.jpg")
                    await ctx.send(file=image)
                logger.info(f"Command `{ctx.command}` invoked with arguments {args}")

    def run(self):
        self.client.run(self.token)

if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    logger = logging.getLogger("discord")

    load_dotenv()
    if len(argv) > 1 and argv[1] == "--url":
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
        bot = DiscordBot(getenv("D_TOKEN"))
        bot.add_commands()
        bot.run()
