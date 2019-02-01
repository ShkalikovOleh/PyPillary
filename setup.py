from setuptools import setup, find_packages
import pypillary

setup(
    name = 'pypillary',
    version = pypillary.__version__,
    author="Oleh Shkalikov",
    author_email="Shkalikov.Oleh@outlook.com",
    description="A python package for Mapillary API",
    install_requires=[
        'requests'
    ]
)