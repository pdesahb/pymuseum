import bs4
import requests

from .base import Scrapper


class RedditScrapper(Scrapper):

    def __init__(self, subreddit, *args, top=None, **kwargs):
        self.subreddit = subreddit
        self.top = top
        super().__init__(*args, **kwargs)

    def get_url(self):
        base_url = f"https://old.reddit.com/r/{self.subreddit}"
        if self.top is None:
            return base_url
        else:
            return f"{base_url}/top/?sort=top&t={self.top}"

    def get_image_path(self, **metadata):
        extension = metadata['url'].split('.')[-1]
        filename = metadata['name'] + '.' + extension
        filename = self.sanitize_filename(filename)
        return str((self.save_path / filename).absolute())

    def get_next_page_url(self):
        next_button = self.page.findAll("span", {"class": "next-button"})[0]
        return next_button.a.attrs['href']

    def get_images(self):
        entries = self.page.findAll('p', {'class': 'title'})
        for entry in entries:
            link = entry.a.attrs['href']
            metadata = {
                'name': entry.a.text,
                'url': link
            }
            if link.split('.')[-1].lower() in ['jpg', 'png', 'bmp']:
                yield link, metadata


    def get_next_page(self):
        next_url = self.get_url() if self.page is None else self.get_next_page_url()
        print(next_url)
        page_req = requests.get(next_url, headers=self.headers)
        if page_req.ok:
            self.page = bs4.BeautifulSoup(page_req.content, 'lxml')
            return True
        return False
