try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Screeps Notify',
    'author': 'Robert Hafner',
    'url': 'https://github.com/tedivm/screeps_notify',
    'download_url': 'https://github.com/tedivm/screeps_notify/releases',
    'author_email': 'tedivm@tedivm.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['screeps_notify'],
    'scripts': [],
    'name': 'screeps_notify'
}

setup(**config)
