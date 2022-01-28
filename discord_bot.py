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

class DiscordBot:
    client = commands.Bot(command_prefix="!")
    token = ''
    memes = []
    templates = []
    def __init__(self, token: str):
        self.token = token
        templates = Templates()
        self.memes = templates.memes
        self.templates = templates.all()

    def getFile(self, meme: str, arguments: list)-> discord.File:
        # TODO, add ASCII option
        text = ' '.join(arguments)
        texts = [text]
        # Template config
        print(self.templates)
        config = self.templates[meme]
        render = PhotoRender(config)
        img = render.getImage()
        byte_im = PILToBytes(img)
        image = discord.File(fp=byte_im, filename='meme.jpg')
        print("made a '" + meme + "' meme")
        return image

    def add_commands(self):
        @self.client.event
        async def on_ready():
            await self.client.change_presence(activity=discord.Game(name="with your balls"))
            print("Started Discord Bot!")

        @self.client.command()
        async def soyjack(ctx: commands.Context, *args):
            image = self.getFile('soyjack', args)
            await ctx.send(file=image)

        @self.client.command()
        async def gigachad(ctx: commands.Context, *args):
            image = self.getFile('gigachad', args)
            await ctx.send(file=image)

        @self.client.command()
        async def chadyes(ctx: commands.Context, *args):
            image = self.getFile('chadyes', args)
            await ctx.send(file=image)

        @self.client.command()
        async def chadno(ctx: commands.Context, *args):
            image = self.getFile('chadno', args)
            await ctx.send(file=image)

    def run(self):
        self.client.run(self.token)

if __name__ == '__main__':
    load_dotenv()
    if len(argv) > 1 and argv[1] == '--url':
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
        bot = DiscordBot(getenv('D_TOKEN'))
        bot.add_commands()
        bot.run()
