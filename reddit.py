from praw import Reddit
from praw.models import Comment
from dotenv import load_dotenv
from os import environ
from html.parser import HTMLParser
import logging
import logging.config
import threading
from queue import SimpleQueue
from wojak_generator.templates import Templates
from wojak_generator.helpers import pick_render, check_env
from wojak_generator.uploader import Uploader

"""
parse html and stuff
"""
class ExtractHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.HTMLDATA = []
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.HTMLDATA = []
    def strip_html(self, html)->str:
        self.clean()
        self.feed(html)
        texts = list(filter(lambda text: "\n" not in text, self.HTMLDATA))
        return texts

# cursed (but more efficient?)
my_html_parser = ExtractHTML()
strip_html = lambda html: my_html_parser.strip_html(html)

"""
holds comment, command, and other stuff to avoid reprocessing and help concurrency
also does some of the parsing
"""
class Command():
    comment: Comment = None # praw comment object of the original command comment
    cmd: str = None         # parsed command name
    arguments: list = []    # split arguments list
    link: str               # full link to comment for debug display
    error: str = None
    reply_text: str
    parent_text: str

    def __init__(self, comment, memes):
        self.link = f"https://reddit.com{comment.permalink}"
        argv = comment.body.split()
        cmd = argv[0]
        if cmd.startswith("!") and cmd[1::] in memes and "wojak-meme-bot" not in [reply.author for reply in comment.replies]:
            self.cmd = cmd[1::]
            self.arguments = argv[1::]
            self.parent_text = strip_html(comment.parent().body_html)
            self.comment = comment


class RedditBot:
    client: Reddit          # Praw client object
    subs: str               # subreddits to look through
    templates: Templates    # templates object
    memes: list             # list of memes
    uploader: Uploader      # for imgur bot stuff
    commands: SimpleQueue   # command objects to be processed
    to_send:  SimpleQueue   # processed comments to post to reddit

    footer = "\n\n^([github](https://github.com/raptor8134/wojak-meme-bot) | [subreddit](https://reddit.com/r/wojakmemebot))"

    def __init__(self, subs: list = ["wojakmemebot"]):
        self.subs = "+".join(subs)
        self.client = Reddit(
            user_agent      = environ["R_USER_AGENT"],
            client_id       = environ["R_CLIENT_ID"],
            client_secret   = environ["R_CLIENT_SECRET"],
            username        = environ["R_USERNAME"],
            password        = environ["R_PASSWORD"],
            check_for_updates = False
        )
        self.templates = Templates()
        self.memes = self.templates.memes
        self.uploader = Uploader(environ["I_CLIENT_ID"])
        self.commands = SimpleQueue()
        self.to_send  = SimpleQueue()

    def get_comments(self):
        while True:
            comments=self.client.subreddit(self.subs).stream.comments(skip_existing=True)
            for comment in comments:
                command = Command(comment, self.memes)
                if command.cmd:
                    logger.info(f"Found command {command.link}")
                    self.commands.put(command)

    def reply(self):
        while True:
            command = self.to_send.get()
            command.comment.reply(f"{command.reply_text}\n{self.footer}")
            logger.info(f"Replied to command {command.link}")

    def process(self, command: Command):
        template = self.templates.one(command.cmd)
        args = command.arguments
        if len(args) > 0 and args[0] == "ascii":
            render = pick_render("ascii", template)
            render.run(command.parent_text)
            reply_text = f"```{render.get()}```"
        else:
            render = pick_render("photo", template)
            render.run(command.parent_text)
            img = render.get()
            link = self.uploader.send(img,\
                        f'r/{command.comment.subreddit.display_name} wojak meme',\
                        'Made using wojak-meme-bot')
            if link and not self.uploader.error:
                reply_text = f"[Here's your meme!]({link})"
            else:
                reply_text = "Error uploading image\n\n```{self.uploader.error}```"
        command.reply_text = reply_text
        render.cleanup()
        return command

    def run(self):
        threading.Thread(target=self.get_comments, name="get",   daemon=True).start()
        threading.Thread(target=self.reply,        name="reply", daemon=True).start()
        while True:
            command = self.commands.get()
            command = self.process(command)
            if command.error:
                logger.error("Error '{command.error}' while processing {command.link}")
            self.to_send.put(command)

if __name__ == "__main__":
    load_dotenv("tokens.env")
    subs = environ["R_SUBREDDITS"].split()

    logging.config.fileConfig("logging.ini", disable_existing_loggers=True)
    logger = logging.getLogger("reddit")

    logger.info(f"Starting reddit bot with subs {subs}")
    bot = RedditBot(subs)
    bot.run()
