from praw import Reddit
from os import getenv
from wojak_generator.templates import Templates
from wojak_generator.render import PhotoRender
from wojak_generator.uploader import Uploader

class RedditBot():
    client: Reddit
    sub = 'politicalcompassmemes'
    footer = "\n\n ^([Github](https://github.com/raptor8134/wojak-meme-bot))"

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

    def poll(self):
        templates = Templates()
        memes = templates.all()
        while True:
            comments = self.client.subreddit(self.sub).stream.comments()
            for comment in comments:
                c = comment.body
                if c.startswith("!") and c[1::] in memes:
                    should_reply = True
                    comment.refresh()
                    filtered_replies = list(filter(lambda reply: reply.author.name != 'wojak-meme-bot', comment.replies))
                    for reply in filtered_replies:
                        print("\033[1mFound a comment:\033[0m")
                        print("\thttps://reddit.com/" + comment.permalink)
                        # This is the comment that wants to be added to the image
                        texts = [comment.parent().body]
                        # Path to template img
                        path = f'{templates.base}/{name}'
                        # Template config
                        template = templates.one(name)
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
                                print("Comment deleted!")
                            else:
                                print("\t\033[1;32m✓ Reply posted\033[0m")

if __name__ == '__main__':
    print("Starting Reddit Bot")
    bot = RedditBot()
    bot.poll()
