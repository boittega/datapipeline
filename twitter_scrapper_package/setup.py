from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

setup(
    name="twitter_scrapper",
    version="0.1.0",
    description="Twitter Scrapper package",
    long_description=readme,
    author="Rafael Bottega",
    author_email="boittega@gmail.com",
    url="",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.7",
)
