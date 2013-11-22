from setuptools import setup, find_packages

try:
    desc_file = open("README.md")
    description = desc_file.read()
except:
    description = ""


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
    install_requires=["requests>=1.1.0"],
    entry_points={'console_scripts':['wunderlist = wunderpy.cli.main:main']}
)