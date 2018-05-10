import abc
import pathlib
import string

import requests


class Scrapper(metaclass=abc.ABCMeta):

    def __init__(self, save_path='./'):
        self.page = None
        self.save_path=pathlib.PosixPath(save_path)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    @abc.abstractmethod
    def get_image_path(self, **metadata):
        pass

    @abc.abstractmethod
    def get_images(self):
        pass

    @abc.abstractmethod
    def get_next_page(self):
        pass

    @staticmethod
    def sanitize_filename(name):
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        return ''.join(c for c in name if c in valid_chars)

    def scrap(self, max_images):
        n_images = 0
        while self.get_next_page():
            for image_link, metadata in self.get_images():
                image_path = self.get_image_path(**metadata)
                if pathlib.Path(image_path).is_file():
                    continue
                image_req = requests.get(image_link, stream=True, headers=self.headers)
                if image_req.status_code == 200:
                    print(n_images, image_link)
                    print(image_path)
                    with open(image_path, 'wb') as image:
                        for chunk in image_req:
                            image.write(chunk)
                    n_images += 1
                    if (n_images >= max_images) and (max_images > 0):
                        return
