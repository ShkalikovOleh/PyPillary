from setuptools import setup
import pypillary
import pypillary.model
import pypillary.request
import pypillary.utils

setup(
    name = 'pypillary',
    version = pypillary.__version__,
    author="Oleh Shkalikov",
    author_email="Shkalikov.Oleh@outlook.com",
    description="A python package for Mapillary API",
    install_requires=[
        'aiohttp',
        'python-dateutil'
    ]
)