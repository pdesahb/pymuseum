import bs4
import click
import requests

from pymuseum.scrapers.base import AbstractScraper
from pymuseum.scrapers import register_cmd


class WikimediaScraper(AbstractScraper):

    def __init__(self, category, *args, **kwargs):
        encoded_category = category.replace(' ', '_')
        self.url = f"https://commons.wikimedia.org/wiki/Category:{encoded_category}"
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_url_from_absolute(absolute):
        return f"https://commons.wikimedia.org{absolute}"

    def get_image_path(self, **metadata):
        extension = metadata['url'].split('.')[-1]
        filename = metadata['name'] + '.' + extension
        filename = self.sanitize_filename(filename)
        return str((self.save_path / filename).absolute())

    def get_next_page_url(self):
        if self.page is None:
            return self.url
        medias = self.page.find(id='mw-category-media')
        next_button = medias.find_all("a")[-1]
        next_url = next_button.attrs['href']
        return self.get_url_from_absolute(next_url)

    def get_images(self):
        entries = self.page.find_all('div', class_='gallerytext')
        for entry in entries:
            entry_link = self.get_url_from_absolute(entry.a.attrs['href'])
            metadata = {
                'name': '.'.join(entry.a.text.split('.')[:-1]),
            }
            entry_page = requests.get(entry_link, headers=self.headers)
            if not entry_page.ok:
                continue
            entry_page = bs4.BeautifulSoup(entry_page.content, "lxml")
            link = entry_page.find(id='file').a.attrs['href']
            metadata['url'] = link
            yield link, metadata


@register_cmd
@click.command('wikimedia')
@click.argument('category', type=click.STRING)
@click.pass_context
def reddit_cmd(ctx, category):
    scraper = WikimediaScraper(category, save_path=ctx.obj['save_path'], dry_run=ctx.obj['dry_run'])
    scraper.scrap(ctx.obj['max_images'])
