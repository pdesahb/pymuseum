import logging
import glob

import tqdm
import cv2

from pymuseum.processing import museumify
from pymuseum.scrappers.reddit import RedditScrapper
from pymuseum.scrappers.artuk import ArtUKScrapper

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.INFO)
# logger.addHandler(stream_handler)


# scrapper = RedditScrapper(subreddit='lepetitmusee', top='all', save_path='/home/pdesahb/Pictures/backgrounds/')
# scrapper.scrap(100)

#scrapper = RedditScrapper(subreddit='museum', top='all', save_path='/home/pdesahb/Pictures/backgrounds/')
#scrapper.scrap(100)

# scrapper = ArtUKScrapper(save_path='/home/pdesahb/Pictures/backgrounds/')
# scrapper.scrap(100)


in_dir = '/home/pdesahb/Pictures/Vincent van Gogh/'
out_dir = '/home/pdesahb/Pictures/backgrounds/Vincent van Gogh/'
for image in tqdm.tqdm(glob.glob(in_dir + '*')):
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    extension = image.split('/')[-1].split('.')[-1]
    title = '.'.join(image.split('/')[-1].split('.')[:-1]) + ' - Vincent van Gogh'
    img = museumify(img, title)
    cv2.imwrite(out_dir + title + '.' + extension, img)
