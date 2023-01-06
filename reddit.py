from praw import Reddit
from praw.models import Comment
from dotenv import load_dotenv
from os import getenv
from html.parser import HTMLParser
import logging
import logging.config
from wojak_generator.templates import Templates
from wojak_generator.helpers import pick_render, check_env
from wojak_generator.uploader import Uploader

class ExtractHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.HTMLDATA = []
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.HTMLDATA = []

class RedditBot():
    client: Reddit
    sub = 'wojakmemebot'
    footer = "\n\n^([Github](https://github.com/raptor8134/wojak-meme-bot))"
    """
    List with all available templates
    """
    memes = []
    """
    JSON config of all available templates
    """
    templates = []
    uploader: Uploader

    def __init__(self, imgur_client_id: str, sub: str = ''):
        self.client = Reddit(
            user_agent      = getenv("R_USER_AGENT"),
            client_id       = getenv("R_CLIENT_ID"),
            client_secret   = getenv("R_CLIENT_SECRET"),
            username        = getenv("R_USERNAME"),
            password        = getenv("R_PASSWORD")
        )
        if sub:
            self.sub = sub
        # Get all memes
        templates = Templates()
        self.memes = templates.memes
        self.templates = templates.all()
        # Set imgur API
        self.uploader = Uploader(imgur_client_id)

    def getMode(self, c_split: list)-> str:
        """
        Returns mode the user sent, defaults to photo if nothing is sent or is invalid
        """
        if len(c_split) > 1:
            return c_split[1]
        return 'photo'

    def send(self, response: str, comment: Comment):
            try:
                comment.reply(response)
            except praw.exceptions.RedditAPIException:
                print("Comment deleted!")
            else:
                print("\t\033[1;32m✓ Reply posted\033[0m")

    def sendPhoto(self, img, comment: Comment):
        """
        Reply with Imgur link
        """
        link = self.uploader.send(render.get(), f'r/{self.sub} wojak meme', 'Made using wojak-meme-bot')
        if link and not self.uploader.error:
            self.send("[Here's your meme!](" + link + ")" + self.footer, comment)
        else:
            self.send(self.uploader.error, comment)

    def sendASCII(self, text: str, comment: Comment):
        """
        Reply with some glorious ASCII art
        """
        # The ``` are useful for markdown, creates a block that makes formatting easier
        self.send(f'```{text}```\n{self.footer}', comment)

    def poll(self):
        while True:
            comments = self.client.subreddit(self.sub).stream.comments()
            for comment in comments:
                c = comment.body
                c_split = c.split()
                command = c_split[0] # !chadyes, for example
                if command.startswith("!") and command[1::] in self.memes:
                    meme = command[1::]
                    comment.refresh()
                    if "wojak-meme-bot" not in [ reply.author for reply in comment.replies ]:
                        logger.debug(f"Found a comment: https://reddit.com{comment.permalink}")
                        # Parse html comment and ignore \n
                        html_parser = ExtractHTML()
                        html_parser.feed(comment.parent().body_html)
                        texts = list(filter(lambda text: '\n' not in text, html_parser.HTMLDATA))
                        template = self.templates[self.memes.index(meme)]
                        mode = self.getMode(c_split) # ascii, for example
                        render = pick_render(mode, template)
                        render.run(texts)
                        if mode == 'photo':
                            self.sendPhoto(render.get(), comment)
                        else:
                            self.sendASCII(render.get(), comment)
                        render.cleanup()

if __name__ == '__main__':
    load_dotenv()
    # Check DotEnv vars first
    required_env = [
        "R_USER_AGENT", "R_CLIENT_ID", "R_CLIENT_SECRET", "R_USERNAME", "R_PASSWORD", "I_CLIENT_ID"
    ]
    check_env(required_env)

    # Get subreddit
    sub = ''
    if getenv('R_SUBREDDIT'):
        sub = getenv('R_SUBREDDIT')
    else: sub = "wojakmemebot" # redundant, but needed for the logging filename

    # logging setup
    logging.config.fileConfig("logging.ini", disable_existing_loggers=True)
    logger = logging.getLogger("reddit")

    logger.info(f"Starting bot on r/{sub}")
    bot = RedditBot(getenv('I_CLIENT_ID'), sub)
    bot.poll()
