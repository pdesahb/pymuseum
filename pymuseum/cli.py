import click

from pymuseum.scrappers import REGISTERED_SCRAPPER_CMD


@click.group('scrap')
@click.option('-to', default='.', type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Directory to save images", show_default=True)
@click.option('-n', type=click.INT, default=5, help="Max number of images to download",
              show_default=True)
@click.pass_context
def scrap(ctx, to, n):
    ctx.obj['save_path'] = to
    ctx.obj['max_images'] = n

for cmd in REGISTERED_SCRAPPER_CMD:
    scrap.add_command(cmd)

@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}

cli.add_command(scrap)
