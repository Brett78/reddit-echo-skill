import praw
import os
from pprint import pprint


class RedditClient(object):
    default_post_limit = 5

    def __init__(self):
        self.client_id = os.environ.get('RS_CLIENT_ID')
        self.client_secret = os.environ.get('RS_CLIENT_SECRET')
        self.username = os.environ.get('RS_USERNAME')
        self.password = os.environ.get('RS_PASSWORD')
        self.validate()
        self.subreddit = 'all'
        self.client = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  username=self.username,
                                  password=self.password,
                                  user_agent='test user agent')

    def validate(self):
        if self.client_id is None \
                or self.client_secret is None \
                or self.username is None \
                or self.password is None:
            raise ValueError('Missing environment variables')

    def get_top_posts(self):
        return "The top reddit posts right now are: " + self.hot_posts_from_subreddit()

    def get_specific_top_posts(self):
        if not self.valid_subreddit():
            return "Sorry I couldn't find {0}".format(self.subreddit)

        return "The top reddit posts right now for {0} are: ".format(self.subreddit) + self.hot_posts_from_subreddit(self.subreddit)

    def hot_posts_from_subreddit(self, subreddit='all'):
        return ". ".join([post.title.replace('.', '') for post in self.client.subreddit(subreddit).hot(limit=RedditClient.default_post_limit)])

    def valid_subreddit(self):
        if self.subreddit is None:
            return False

        try:
            found = self.client.subreddits.search_by_name(self.subreddit, exact=True)
        except Exception:
            found = False

        return found

