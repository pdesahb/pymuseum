import abc
import io
import logging
import pathlib
import unicodedata

import bs4
import requests

from pymuseum import processing


class AbstractScraper(metaclass=abc.ABCMeta):

    def __init__(self, save_path='./', dry_run=False):
        self.logger = logging.getLogger('pymuseum')
        self.dry_run = dry_run
        self.page = None
        self.save_path=pathlib.PosixPath(save_path)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    @staticmethod
    def sanitize_filename(name):
        # remove accents
        name = ''.join(c for c in unicodedata.normalize('NFD', name)
                       if unicodedata.category(c) != 'Mn')
        # replace special characters
        replacements = {
            '–': '-'
        }
        for old, new in replacements.items():
            name = name.replace(old, new)
        # delete invalid chars
        invalid_chars = f"/"
        name =  ''.join(c for c in name if c not in invalid_chars)
        return name

    @abc.abstractmethod
    def get_image_path(self, **metadata):
        pass

    @abc.abstractmethod
    def get_images(self):
        pass

    @abc.abstractmethod
    def get_next_page_url(self):
        pass

    def get_next_page(self):
        next_url = self.get_next_page_url()
        page_req = requests.get(next_url, headers=self.headers)
        if page_req.ok:
            self.page = bs4.BeautifulSoup(page_req.content, 'lxml')
            return True
        return False

    def scrap(self, max_images):
        n_images = 0
        self.logger.info('loading %s', self.get_next_page_url())
        while self.get_next_page():
            for image_link, metadata in self.get_images():
                image_path = self.get_image_path(**metadata)
                self.logger.debug('saving %s to %s', image_link, image_path)
                if pathlib.Path(image_path).is_file():
                    continue
                try:
                    image_req = requests.get(image_link, stream=True, headers=self.headers)
                except requests.exceptions.ConnectionError:
                    self.logger.info('could not connect to %s', image_link)
                    continue
                if (image_req.status_code == 200) and not self.dry_run:
                    image = io.BytesIO()
                    for chunk in image_req:
                        image.write(chunk)
                    *title, extension = image_path.split('/')[-1].split('.')
                    title = '.'.join(title)
                    image = processing.museumify_bytes(image, title, '.'+extension)
                    with open(image_path, 'wb') as image_file:
                        image.seek(0)
                        image_file.write(image.read())
                    n_images += 1
                if self.dry_run:
                    n_images += 1
                if (n_images > max_images) and (max_images > 0):
                    return
            self.logger.info('got %d/%d images', n_images, max_images)
