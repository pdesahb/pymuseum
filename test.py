from background.scrappers.reddit import RedditScrapper
from background.scrappers.artuk import ArtUKScrapper


scrapper = ArtUKScrapper(save_path='/home/pdesahb/Pictures/background/raw/')
scrapper.scrap(100)
