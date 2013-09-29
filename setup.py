from setuptools import setup, find_packages

with open("README.md") as file:
    description = file.read()


setup(
    name="wunderpy",
    version="0.2.0",
    author="bsmt",
    author_email="bsmt@bsmt.me",
    url="https://github.com/bsmt/wunderpy",
    license="LICENSE",
    description="An experimental wrapper for the Wunderlist 2 API",
    long_description=description,
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests>=1.1.0", "nose>=1.3.0", "nose-testconfig>=0.9"]
)