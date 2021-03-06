import bs4
import click
import requests

from pymuseum.scrapers.base import AbstractScraper
from pymuseum.scrapers import register_cmd


class Redditscraper(AbstractScraper):

    def __init__(self, subreddit, *args, top=None, **kwargs):
        base_url = f"https://old.reddit.com/r/{subreddit}"
        self.url = base_url if top is None else f"{base_url}/top/?sort=top&t={top}"
        super().__init__(*args, **kwargs)

    def get_image_path(self, **metadata):
        extension = metadata['url'].split('.')[-1]
        filename = metadata['name'] + '.' + extension
        filename = self.sanitize_filename(filename)
        return str((self.save_path / filename).absolute())

    def get_next_page_url(self):
        if self.page is None:
            return self.url
        next_button = self.page.find_all("span", class_="next-button")[0]
        return next_button.a.attrs['href']

    def get_images(self):
        entries = self.page.find_all('p', class_='title')
        for entry in entries:
            link = entry.a.attrs['href']
            metadata = {
                'name': entry.a.text,
                'url': link
            }
            if link.split('.')[-1].lower() in ['jpg', 'png', 'bmp']:
                yield link, metadata


@register_cmd
@click.command('reddit')
@click.argument('subreddit', type=click.STRING)
@click.option('-top', type=click.Choice(['hour', 'day', 'month', 'year', 'all']),
              help="whether to scrap the top of the subreddit")
@click.pass_context
def reddit_cmd(ctx, subreddit, top):
    scraper = Redditscraper(subreddit, top=top, save_path=ctx.obj['save_path'], dry_run=ctx.obj['dry_run'])
    scraper.scrap(ctx.obj['max_images'])
