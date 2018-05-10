import logging

from pymuseum.scrappers.reddit import RedditScrapper
from pymuseum.scrappers.artuk import ArtUKScrapper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


scrapper = RedditScrapper(subreddit='lepetitmusee', top='all', save_path='/home/pdesahb/Pictures/backgrounds/')
scrapper.scrap(100)

#scrapper = RedditScrapper(subreddit='museum', top='all', save_path='/home/pdesahb/Pictures/backgrounds/')
#scrapper.scrap(100)

# scrapper = ArtUKScrapper(save_path='/home/pdesahb/Pictures/backgrounds/')
# scrapper.scrap(100)
