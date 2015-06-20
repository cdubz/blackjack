try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Blackjack',
    'author': 'Christopher Charbonneau Wells',
    'url': 'https://github.com/cdubz/blackjack',
    'download_url': 'https://github.com/cdubz/blackjack/archive/master.zip',
    'author_email': 'chris.wells@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['blackjack'],
    'scripts': [],
    'name': 'blackjack'
}

setup(**config)
