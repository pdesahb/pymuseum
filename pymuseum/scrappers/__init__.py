from os.path import basename, dirname, join
from glob import glob

REGISTERED_SCRAPPER_CMD = []

def register_cmd(cmd):
    REGISTERED_SCRAPPER_CMD.append(cmd)
    return cmd

pwd = dirname(__file__)
for x in glob(join(pwd, '*.py')):
    if not x.startswith('__'):
        module_name = 'pymuseum.scrappers.' + basename(x)[:-3]
        __import__(module_name, globals(), locals())


__all__ = [
    'REGISTERED_SCRAPPER_CMD'
]
