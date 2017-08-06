from reddit_client import RedditClient
from alexa_handler import AlexaHandler
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
event_handler = AlexaHandler()


@event_handler.intent('GetTopPosts')
def get_top_posts():
    reddit_client = RedditClient()
    return reddit_client.get_top_posts()


@event_handler.intent('GetSpecificTopPosts')
def get_specific_top_posts():
    reddit_client = RedditClient()
    reddit_client.subreddit = event_handler.get_params().get('SubReddit', {}).get('value')
    return reddit_client.get_specific_top_posts()


def lambda_handler(event, context):
    logging.info('Executing lambda function')
    return event_handler.process_request(event)
