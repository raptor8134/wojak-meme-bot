from praw import Reddit
from dotenv import load_dotenv
from os import getenv
from html.parser import HTMLParser
import logging
from wojak_generator.templates import Templates
from wojak_generator.render import PhotoRender
from wojak_generator.uploader import Uploader
from wojak_generator.helpers import check_env

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
    footer = "\n\n ^([Github](https://github.com/raptor8134/wojak-meme-bot))"
    memes = []
    templates = []

    def __init__(self, sub: str = ''):
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

    def poll(self):
        while True:
            comments = self.client.subreddit(self.sub).stream.comments()
            for comment in comments:
                c = comment.body
                if c.startswith("!") and c[1::] in self.memes:
                    meme = c[1::]
                    comment.refresh()
                    if "wojak-meme-bot" not in [ reply.author for reply in comment.replies ]:
                        logger.debug(f"Found a comment: https://reddit.com{comment.permalink}")
                        # Parse html comment and ignore \n
                        html_parser = ExtractHTML()
                        html_parser.feed(comment.parent().body_html)
                        texts = list(filter(lambda text: '\n' not in text, html_parser.HTMLDATA))
                        #template = self.templates[meme]
                        template = self.templates[self.memes.index(meme)]
                        path = f'{Templates.base}/{meme}/template.jpg'
                        render = PhotoRender(path, template)
                        uploader = Uploader()

                        render.run(texts)
                        link = uploader.send(render.getImage(), f'r/{self.sub} wojak meme', '')
                        render.cleanup()
                        if link:
                            try:
                                comment.reply(\
                                    "[Here's your meme!](" + link + ")" + self.footer)
                            except praw.exceptions.RedditAPIException:
                                logger.error("Comment was deleted!", exc_info=True)
                            else:
                                logger.debug("Reply posted")

if __name__ == '__main__':
    load_dotenv()
    # Check DotEnv vars first
    required_env = [
        "R_USER_AGENT", "R_CLIENT_ID", "R_CLIENT_SECRET", "R_USERNAME", "R_PASSWORD"
    ]
    check_env(required_env)

    # Get subreddit
    sub = ''
    if getenv('R_SUBREDDIT'):
        sub = getenv('R_SUBREDDIT')
    else: sub = "wojakmemebot" # redundant, but needed for the logging filename

    # logging setup, have to do after the getenv stuff for the correct filename
    logger = logging.getLogger(sub)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        handlers = [
            logging.FileHandler("./logs/reddit.log"),
            logging.StreamHandler()
        ]
    )
    logger.info(f"Starting bot on r/{sub}")

    bot = RedditBot(sub)
    bot.poll()
