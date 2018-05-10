import bs4
import requests

from .base import Scrapper


class ArtUKScrapper(Scrapper):

    def __init__(self, *args, **kwargs):
        self.url = "https://artuk.org/discover/artworks"
        super().__init__(*args, **kwargs)

    def get_image_path(self, **metadata):
        extension = metadata['url'].split('.')[-1]
        filename = metadata['title'] + ' - ' + metadata['artist'] + '.' + extension
        filename = self.sanitize_filename(filename)
        return str((self.save_path / filename).absolute())

    def get_next_page_url(self):
        return self.url

    def get_images(self):
        entries = self.page.find_all('li', class_='item')
        for entry in entries:
            infos = entry.find_all('div', class_='info')[0]
            title = infos.find_all('div', class_="title")[0]
            artist = infos.find_all('div', class_="artist")[0]
            metadata = {
                'artist': artist.text,
                'title': title.text
            }
            entry_link = entry.a.attrs['href']
            entry_page = requests.get(entry_link, headers=self.headers)
            if not entry_page.ok:
                continue
            entry_page = bs4.BeautifulSoup(entry_page.content, "lxml")
            link = entry_page.find_all('div', class_='artwork')[0].img.attrs['src']
            metadata['url'] = link
            yield link, metadata
