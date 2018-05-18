import glob
import pathlib

import click

from pymuseum.scrapers import REGISTERED_SCRAPER_CMD
from pymuseum.processing import museumify_file


@click.group('scrap')
@click.option('-to', default='.', type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Directory to save images", show_default=True)
@click.option('-n', type=click.INT, default=5, help="Max number of images to download",
              show_default=True)
@click.pass_context
def scrap(ctx, to, n):
    ctx.obj['save_path'] = to
    ctx.obj['max_images'] = n

for cmd in REGISTERED_SCRAPER_CMD:
    scrap.add_command(cmd)


@click.command('transform')
@click.argument('images', type=click.STRING)
@click.option('-to', default='.', type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Directory to save results to", show_default=True)
@click.option('-set-title/-no-title', default=True, show_default=True,
              help="whether to include the image title into the wallpaper")
def transform(images, to, set_title):
    for file_in in glob.glob(images):
        path_in = pathlib.Path(file_in)
        file_out = str(pathlib.Path(to) / path_in.name)
        title = path_in.stem if set_title else ''
        museumify_file(file_in, file_out, title)



@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}

cli.add_command(transform)
cli.add_command(scrap)
