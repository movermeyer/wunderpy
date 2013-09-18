from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name="wunderpy",
    version="0.2.0",
    author="bsmt",
    author_email="bsmt@krax.in",
    url="https://github.com/bsmt/wunderpy",
    license="LICENSE",
    description="An experimental wrapper for the Wunderlist 2 API",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=required
)